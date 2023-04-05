# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ActivityCancelWizard(models.TransientModel):
    _name = "activity.cancel.wizard"
    _description = "Activity Cancel Wizard"

    activity_id = fields.Many2one('mail.activity', string='Activity')

    def action_cancel(self):
        active_ids = self._context.get('active_ids')
        for rec in self:
            for active_id in active_ids:
                activity_id = self.env['mail.activity'].search([('id', '=', active_id)])
                activity_id.action_cancel_activity()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
