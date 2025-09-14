# Copyright 2025 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command
from odoo.tests import TransactionCase


class TestNewChannel(TransactionCase):
    def test_create_new_channel(self):
        lang_fr = self.env.ref("base.lang_fr")
        lang_fr.active = True
        lang_en = self.env.ref("base.lang_en")
        wizard = self.env["shopinvader.new.channel.wizard"].create(
            {
                "name": "My Super Shop",
                "se_backend_type": "elasticsearch",
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
        channel = wizard.run()
        self.assertEqual(channel.name, "My Super Shop")
