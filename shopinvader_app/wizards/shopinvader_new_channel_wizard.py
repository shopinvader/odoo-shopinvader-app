# Copyright 2025 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import urllib.parse
from urllib.parse import urlparse

from odoo import fields, models
from odoo.fields import Command

from odoo.addons.http_routing.models.ir_http import slugify

from .elasticsearch_config import (
    ES_DEFAULT_BRAND_CONFIG,
    ES_DEFAULT_CATEGORY_CONFIG,
    ES_DEFAULT_PRODUCT_CONFIG,
)


class ShopinvaderNewChannelWizard(models.TransientModel):
    _name = "shopinvader.new.channel.wizard"
    _description = "Shopinvader New Channel Wizard"

    name = fields.Char(related="channel_id.name")
    channel_id = fields.Many2one(
        "sale.channel",
        "Channel",
        default=lambda self: self.env.context.get("active_id"),
    )
    se_backend_type = fields.Selection(
        selection=lambda self: self.env["se.backend"]._fields["backend_type"].selection,
        string="Search Engine Type",
        required=True,
    )
    se_backend_host = fields.Char(
        string="Search Engine Host",
        required=True,
    )
    lang_ids = fields.Many2many(
        comodel_name="res.lang",
        string="Lang",
        default=lambda self: self.env["res.lang"].search([("active", "=", True)]),
    )
    model_ids = fields.Many2many(
        comodel_name="ir.model",
        string="Model",
        domain=lambda self: self.env["se.index"]._model_id_domain(),
        default=lambda self: self.env["ir.model"].search(
            self.env["se.index"]._model_id_domain()
        ),
    )
    frontend_public_url = fields.Char()

    def _get_serializer_type(self, model):
        return {
            "product.product": "shopinvader_product_exports",
            "product.category": "shopinvader_category_exports",
            "product.brand": "shopinvader_brand_exports",
        }[model.model]

    def _get_config(self, model):
        if self.se_backend_type == "elasticsearch":
            body = {
                "product.product": ES_DEFAULT_PRODUCT_CONFIG,
                "product.category": ES_DEFAULT_CATEGORY_CONFIG,
                "product.brand": ES_DEFAULT_BRAND_CONFIG,
            }[model.model]
        elif self.se_backend_type == "typesense":
            body = {"fields": [{"name": "name", "type": "string"}]}
        if body:
            config = self.env["se.index.config"].create(
                {
                    "name": f"{self.name} - {model.name}",
                }
            )
            # TODO solve issue in search-engine with the default
            # value of body_str
            config.body = body
            return config
        return self.env["se.index.config"]

    def _prepare_index_vals(self, model, lang):
        return {
            "lang_id": lang.id,
            "model_id": model.id,
            "serializer_type": self._get_serializer_type(model),
            "config_id": self._get_config(model).id,
        }

    def _get_or_create_size(self, size_vals):
        size = self.env["se.thumbnail.size"].search(
            [
                ("name", "=", size_vals[0]),
                ("size_x", "=", size_vals[1]),
                ("size_y", "=", size_vals[2]),
            ]
        )
        if size:
            return size
        else:
            return self.env["se.thumbnail.size"].create(
                {
                    "name": size_vals[0].title(),
                    "key": size_vals[0],
                    "size_x": size_vals[1],
                    "size_y": size_vals[2],
                }
            )

    def _prepare_thumbnail_vals(self, model):
        default_sizes = [
            ("small", 60, 60),
            ("medium", 300, 300),
            ("large", 600, 600),
            ("xlarge", 1000, 1000),
        ]
        xmlid = {
            "product.product": (
                "fs_product_multi_image.field_product_product__variant_image_ids"
            ),
            "product.category": (
                "fs_product_multi_image.field_product_category__image_ids"
            ),
            "product.brand": (
                "fs_product_brand_multi_image.field_product_brand__image_ids"
            ),
        }[model.model]
        field = self.env.ref(xmlid)
        return {
            "model_id": model.id,
            "field_id": field.id,
            "size_ids": [self._get_or_create_size(size).id for size in default_sizes],
        }

    def _create_api_user(self):
        xml_groups = [
            "fastapi.group_fastapi_endpoint_runner",
            "shopinvader_api_address.shopinvader_address_user_group",
            "shopinvader_api_delivery_carrier.shopinvader_delivery_carrier_user_group",
            "shopinvader_api_sale_loyalty.shopinvader_loyalty_user_group",
            "shopinvader_api_security_sale.shopinvader_sale_user_group",
            "shopinvader_api_security_sale.shopinvader_sale_user_group",
        ]
        groups = self.env["res.groups"]
        for xml in xml_groups:
            if group := self.env.ref(xml, raise_if_not_found=False):
                groups |= group
        name = f"{self.name} API User"
        return self.env["res.users"].create(
            {
                "name": name,
                "login": slugify(name),
                "groups_id": [Command.set(groups.ids)],
            }
        )

    def _create_directory(self):
        return self.env["auth.directory"].create(
            {
                "name": self.name,
            }
        )

    def run(self):
        indexes = []
        thumbnails = []
        for model in self.model_ids:
            for lang in self.lang_ids:
                indexes.append(Command.create(self._prepare_index_vals(model, lang)))
            thumbnails.append(Command.create(self._prepare_thumbnail_vals(model)))

        ssl = self.se_backend_host.startswith("https")

        vals = {
            "name": self.name,
            "backend_type": self.se_backend_type,
            "index_ids": indexes,
            "image_field_thumbnail_size_ids": thumbnails,
            "image_data_url_strategy": "storage_url",
            "ssl": ssl,
        }
        if self.se_backend_type == "elasticsearch":
            vals["es_server_host"] = self.se_backend_host
        elif self.se_backend_type == "typesense":
            host = urlparse(self.se_backend_host)
            vals.update(
                {
                    "ts_server_host": host.hostname,
                    "ts_server_port": host.port,
                    "ts_server_protocol": host.scheme,
                    "ts_api_key": "xyz",  # default password
                }
            )
        se_backend = self.env["se.backend"].create(vals)
        for index in se_backend.index_ids:
            if index.config_id:
                index.export_settings()
        self.channel_id.search_engine_id = se_backend.id
        root_path = f"/shopinvader-api/{slugify(self.name)}"
        endpoint = self.env["fastapi.endpoint"].create(
            {
                "name": self.name,
                "app": "shopinvader",
                "root_path": root_path,
                "user_id": self._create_api_user().id,
                "save_http_session": False,
                "directory_id": self._create_directory().id,
                "sale_channel_id": self.channel_id.id,
                "public_url": self.frontend_public_url,
                "public_api_url": urllib.parse.urljoin(
                    self.frontend_public_url, root_path
                ),
            }
        )
        # sync endpoint twice
        # see issue : https://github.com/OCA/rest-framework/issues/391
        endpoint.action_sync_registry()
        endpoint.action_sync_registry()
        return True
