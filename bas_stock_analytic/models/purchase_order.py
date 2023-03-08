# -*- coding: utf-8 -*-
# Part of BAS. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_is_zero, float_compare
from datetime import datetime
from collections import namedtuple, OrderedDict, defaultdict

class PurchaseOrder(models.Model):

    _inherit = ["purchase.order", 'analytic.mixin']
    _name = "purchase.order"

    analytic_distribution = fields.Json('Analytic', copy=True,
                                        readonly=True,
                                        states={'draft': [('readonly', False)]})

    @api.onchange('analytic_distribution')
    def onchange_analytic_distribution(self):
        for line in self.order_line.filtered(lambda r: r.display_type not in ['line_section', 'line_note']):
            line.update({
                'analytic_distribution': self.analytic_distribution
            })
    

