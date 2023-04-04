# -*- coding: utf-8 -*-
from datetime import datetime

from odoo.tools.misc import clean_context
from odoo import api, fields, models, _


class InheritedMailActivity(models.Model):
    _inherit = 'mail.activity'

    supervisor_id = fields.Many2one('res.users', string='Supervisor')
    tag_ids = fields.Many2many('activity.tag', 'rel_activity_ad_tag', 'activity_id', 'tag_id', string="Activity Tag")
    date_done = fields.Datetime(string="Complete Date")
    is_cancel = fields.Boolean(string='Is Cancel')
    state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], 'status', store=True
    )
    feedback = fields.Char('Feedback')
    is_multi_user = fields.Boolean(string='Display Multi Users',
                                   default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                       'activities_management_app.is_multi_user'))
    multi_user_ids = fields.Many2many('res.users', 'rel_mail_activity_multi_user', 'activity_id', 'user_id',
                                      string='Multi User')
    state_process = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'Progress'),
        ('done', 'Done')], string="Delay units",
        default='draft')

    @api.depends('date_deadline', 'feedback')
    def _compute_state(self):
        for record in self.filtered(lambda activity: activity.date_deadline):
            tz = record.user_id.sudo().tz
            date_deadline = record.date_deadline
            if record.is_cancel:
                record.state = 'cancel'
            elif record.feedback:
                record.state = 'done'
            else:
                record.state = self._compute_state_from_date(date_deadline, tz)

    def action_done(self):
        """ Wrapper without feedback because web button add context as
        parameter, therefore setting context to feedback """
        return {
            'type': 'ir.actions.act_window',
            'name': _('Feedback'),
            'res_model': 'activity.feedback.wizard',
            'view_mode': 'form',
            'context': {'default_activity_id': self.id},
            'target': 'new'}
        # return messages.ids and messages.ids[0] or False

    def action_cancel_activity(self):
        for rec in self:
            print('Hello')
            rec.is_cancel = True
            rec._compute_state()

    def action_open_doc(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Activity Origin'),
            'res_model': self.res_model,
            'view_mode': 'tree,form',
            'domain': [('id', '=', self.res_id)],
            'context': {'create': 0},
            'targer': 'new'}

    def action_close_dialog(self):
        res = super(InheritedMailActivity, self).action_close_dialog()

        if self.multi_user_ids:
            for order in self.multi_user_ids:
                if not self.activity_type_id.category in ('meeting'):
                    if self.state_process == 'draft':
                        self.create({
                            'activity_type_id': self.activity_type_id.id,
                            'date_deadline': self.date_deadline,
                            'multi_user_ids': self.multi_user_ids,
                            'user_id': order.id,
                            'note': self.note,
                            'is_multi_user': self.is_multi_user,
                            'summary': self.summary,
                            'state_process': 'progress'})

                    elif self.state_process == 'progress':
                        result = self.env['mail.activity'].browse(self.id)

                        result.write({
                            'activity_type_id': self.activity_type_id.id,
                            'date_deadline': self.date_deadline,
                            'multi_user_ids': self.multi_user_ids,
                            'is_multi_user': self.is_multi_user,
                            'user_id': order.id,
                            'note': self.note,
                            'summary': self.summary})

                else:
                    if self.state_process == 'draft':
                        self.create({
                            'activity_type_id': self.activity_type_id.id,
                            'user_id': order.id,
                            'multi_user_ids': self.multi_user_ids,
                            'summary': self.summary,
                            'is_multi_user': self.is_multi_user,
                            'state_process': 'progress'})

                    elif self.state_process == 'progress':
                        result = self.env['mail.activity'].browse(self.id)

                        result.write({
                            'activity_type_id': self.activity_type_id.id,
                            'user_id': order.id,
                            'is_multi_user': self.is_multi_user,
                            'multi_user_ids': self.multi_user_ids,
                            'summary': self.summary})

        return res

    def _check_access_assignation(self):
        for activity in self:
            model = self.env[activity.res_model].with_user(
                activity.user_id)

    def action_feedback_schedule_next(self, feedback=False):
        ctx = dict(
            clean_context(self.env.context),
            default_previous_activity_type_id=self.activity_type_id.id,
            activity_previous_deadline=self.date_deadline,
            default_res_id=self.res_id,
            default_res_model=self.res_model,
        )
        self.feedback = 'Schedule Next Activity'
        self.date_done = datetime.today()
        return {
            'name': _('Schedule an Activity'),
            'context': ctx,
            'view_mode': 'form',
            'res_model': 'mail.activity',
            'views': [(False, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
