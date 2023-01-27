 # -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class CrmLead(models.Model):
    _inherit = "crm.lead"

    lead_number = fields.Char(
        string="Lead Number",
        copy=False,
        readonly=True
    )

    
    @api.model
    def create(self, vals): 
        vals['lead_number'] = self.env['ir.sequence'].next_by_code('crm.lead')
        return super(CrmLead,self).create(vals)