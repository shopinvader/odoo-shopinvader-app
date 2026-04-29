# Copyright 2025 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import werkzeug.urls

from odoo.fields import Command
from odoo.tests import TransactionCase
from odoo.tests.common import _super_send


class TestNewChannel(TransactionCase):
    @classmethod
    def _request_handler(cls, s, r, /, **kw):
        url = werkzeug.urls.url_parse(r.url)
        if url.host == "elastic" and url.port == 9200:
            # We need to override the request handler to avoid raising on non
            # localhost host: elastic
            return _super_send(s, r, **kw)
        return super()._request_handler(s, r, **kw)

    def test_create_new_channel(self):
        lang_fr = self.env.ref("base.lang_fr")
        lang_fr.active = True
        lang_en = self.env.ref("base.lang_en")
        channel = self.env["sale.channel"].create({"name": "My Super Shop"})
        wizard = self.env["shopinvader.new.channel.wizard"].create(
            {
                "name": "My Super Shop",
                "channel_id": channel.id,
                "se_backend_type": "elasticsearch",
                "se_backend_host": "http://elastic:9200",
                "lang_ids": [
                    Command.set(
                        [
                            lang_fr.id,
                            lang_en.id,
                        ]
                    ),
                ],
                # Pour les modèles on peut les mettre en automatique
                # + deplacer la logique dans
                "model_ids": [
                    Command.set(
                        [
                            self.env.ref("product.model_product_product").id,
                            self.env.ref("product.model_product_category").id,
                        ]
                    ),
                ],
                "frontend_public_url": "http://my-super-shop.fr",
            }
        )
        self.assertTrue(wizard.run())
        self.assertEqual(channel.name, "My Super Shop")
