# -*- coding: utf-8 -*-
# Part of BAS. See LICENSE file for full copyright and licensing details.

import logging
from odoo import fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_is_zero, float_compare
from datetime import datetime
from collections import namedtuple, OrderedDict, defaultdict

_logger = logging.getLogger(__name__)



    
class SaleOrderLine(models.Model):
    
    _inherit = 'sale.order.line'


    def _prepare_procurement_values(self,group_id):
        res = super(SaleOrderLine,self)._prepare_procurement_values(group_id=group_id)
        _logger.info('bas _prepare_procurement_values : self %s',self)
        _logger.info('bas _prepare_procurement_values : analytic distribution %s',self.analytic_distribution)

        res.update({
                'analytic_distribution': self.analytic_distribution,
            })
        _logger.info('bas _prepare_procurement_values : res %s',res)
        return res
    

