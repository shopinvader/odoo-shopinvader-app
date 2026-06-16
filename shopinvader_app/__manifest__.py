# Copyright 2025 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Shopinvader App",
    "summary": """
        Shopinvader out-of-box ready project
        This include
        - Sale Channel
        - Catalog synchronisation
        - API for common case (cart, sale, picking, invoice...)
        - Custom payment provider
        """,
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion",
    "website": "https://github.com/shopinvader/odoo-shopinvader-app",
    "depends": [
        "sale_channel_search_engine_category",
        "sale_channel_search_engine_product",
        "shopinvader_anonymous_partner",
        "shopinvader_api_address",
        "shopinvader_api_cart",
        "shopinvader_api_customer",
        "shopinvader_api_delivery_carrier",
        "shopinvader_api_payment_cart",
        "shopinvader_api_payment_provider_custom",
        "shopinvader_api_sale",
        "shopinvader_api_settings",
        "shopinvader_sale_channel",
        "shopinvader_fastapi_auth_partner",
        "shopinvader_product_description",
        "shopinvader_product_seo",
        "shopinvader_product_url",
        "shopinvader_product",
        "shopinvader_search_engine_product_price",
        "shopinvader_search_engine_product_stock_state",
        "shopinvader_search_engine_update_image",
        "shopinvader_search_engine_update_product_template_multi_link",
    ],
    "external_dependencies": {"python": ["fastapi"]},
    "data": [
        "views/res_config_settings_views.xml",
        "wizards/shopinvader_new_channel_wizard_view.xml",
        "views/sale_channel_view.xml",
        "security/ir.model.access.csv",
        "data/fs_storage.xml",
    ],
    "application": True,
}
