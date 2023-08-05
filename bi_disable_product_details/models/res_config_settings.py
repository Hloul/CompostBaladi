# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    disable_shop_page_details = fields.Boolean(string="Disable details on shop/product page", related='website_id.disable_shop_page_details', readonly=False)
    disable_option_for_user = fields.Selection(string="Disable Options", related='website_id.disable_option_for_user', readonly=False)
    disable_product_price = fields.Boolean(string='Disable Product price', related='website_id.disable_product_price', readonly=False)
    disable_qty_option = fields.Boolean(string='Disable Qty Option', related='website_id.disable_qty_option', readonly=False)
    disable_add_to_cart = fields.Boolean(string='Disable Add to cart button', related='website_id.disable_add_to_cart', readonly=False)
