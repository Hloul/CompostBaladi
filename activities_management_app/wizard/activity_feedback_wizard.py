# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models, api, _


class ActivityFeedbackWizard(models.TransientModel):
    _name = "activity.feedback.wizard"
    _description = "Activity Feedback Wizard"

    feedback = fields.Char('Feedback',required=True)
    activity_id = fields.Many2one('mail.activity', string='Activity')

    def action_done(self):
        active_ids = self._context.get('active_ids')
        for rec in self:
            for active_id in active_ids:
                activity_id = self.env['mail.activity'].search([('id','=',active_id)])
                activity_id.feedback = rec.feedback
                activity_id.date_done = datetime.today()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
