# Copyright 2025 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    search_engine_id = fields.Many2one(
        readonly=True,
    )
    fastapi_endpoint_ids = fields.One2many(
        "fastapi.endpoint",
        "sale_channel_id",
        "Fastapi Endpoint",
        readonly=True,
    )

    # Following field is only here to improve the usability
    # We do not have o2o field/widget
    fastapi_endpoint_id = fields.Many2one(
        "fastapi.endpoint",
        "Fastapi Endpoint",
        compute="_compute_fastapi_endpoint",
    )

    def _compute_fastapi_endpoint(self):
        for record in self:
            record.fastapi_endpoint_id = fields.first(record.fastapi_endpoint_ids)
