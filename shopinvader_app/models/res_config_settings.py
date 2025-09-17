# Copyright 2025 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_shopinvader_api_sale_loyalty = fields.Boolean("Install Sale Loyalty API")
    module_shopinvader_api_wishlist = fields.Boolean("Install Wishlist API")
