# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': "Website Hide Price, Add to Cart and Qty on Shop ",
    'version': '16.0.0.1',
    "category": 'Website',
    'summary': 'Website Disable Price on website disable Add to Cart on website disable product Quantity on website hide Price on website hide Add to Cart button on website hide product Quantity on shop hide Price on shop hide Add to Cart button on shop hide product qty',
    'description': """

        Disable Price, Qty and Add to Cart Option on Shop in odoo,
        Disable Product Details for Non Login User in odoo,
        Disable Product Details for All Users in odoo,
        Disable Product Price in odoo,
        Disable Add to Cart in odoo,
        Disable Qty Option in odoo,
        Disable Product Details in odoo,

    """,
    'author': 'BrowseInfo',
    "price": 9,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.in',
    'depends': ['base', 'website','website_sale'],
    'data': [
        'views/res_config_settings_view.xml',
        'templates/shop.xml',
    ],
    "license": 'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/9ie9TDgezj0',
    "images":['static/description/Banner.gif'],
}
