# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_disable_options_info(self):
        self.ensure_one()
        product_info = {
            'product_price': False,
            'qty': False,
            'add_to_cart': False,
        }
        current_website = self.env['website'].get_current_website()
        if current_website.disable_shop_page_details:
            if current_website.disable_option_for_user == 'public':
                if self.env.user.has_group('base.group_public'):
                    product_info = {
                        'product_price': True if current_website.disable_product_price else False,
                        'qty': True if current_website.disable_qty_option else False,
                        'add_to_cart': True if current_website.disable_add_to_cart else False,
                    }
                    return product_info
                else:
                    return product_info
            elif current_website.disable_option_for_user == 'all':
                product_info = {
                    'product_price': True if current_website.disable_product_price else False,
                    'qty': True if current_website.disable_qty_option else False,
                    'add_to_cart': True if current_website.disable_add_to_cart else False,
                }
                return product_info
            else:
                return product_info
        else:
            return product_info
