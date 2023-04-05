# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    is_multi_user = fields.Boolean(string='Display Multi Users')
    counter_all_activity = fields.Boolean(string='All Activity')
    counter_plan_activity = fields.Boolean(string='Planned Activity')
    counter_overdue_activity = fields.Boolean(string='Overdue Activity')
    counter_today_activity = fields.Boolean(string='Today Activity')
    counter_done_activity = fields.Boolean(string='Done Activity')
    counter_cancel_activity = fields.Boolean(string='Cancel Activity')

    data_table_all_activity = fields.Boolean(string='All Activity')
    data_table_plan_activity = fields.Boolean(string='Planned Activity')
    data_table_overdue_activity = fields.Boolean(string='Overdue Activity')
    data_table_today_activity = fields.Boolean(string='Today Activity')
    data_table_done_activity = fields.Boolean(string='Done Activity')
    data_table_cancel_activity = fields.Boolean(string='Cancel Activity')

    plan_activity_table_limit = fields.Integer(string='Planned Activity Table Limit')
    all_activity_table_limit = fields.Integer(string='All Activity Table Limit')
    complete_activity_table_limit = fields.Integer(string='Completed Activity Table Limit')
    due_activity_table_limit = fields.Integer(string='Due Activity Table Limit')

    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.is_multi_user', self.is_multi_user)
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.data_table_all_activity',
                                                         self.data_table_all_activity)
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.data_table_plan_activity',
                                                         self.data_table_plan_activity)
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.data_table_overdue_activity',
                                                         self.data_table_overdue_activity)
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.data_table_today_activity',
                                                         self.data_table_today_activity)
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.data_table_done_activity',
                                                         self.data_table_done_activity)
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.data_table_cancel_activity',
                                                         self.data_table_cancel_activity)

        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.counter_plan_activity',
                                                         self.counter_plan_activity)
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.counter_all_activity',
                                                         self.counter_all_activity)
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.counter_overdue_activity',
                                                         self.counter_overdue_activity)
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.counter_today_activity',
                                                         self.counter_today_activity)
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.counter_done_activity',
                                                         self.counter_done_activity)
        self.env['ir.config_parameter'].sudo().set_param('activities_management_app.counter_cancel_activity',
                                                         self.counter_cancel_activity)
        super(ResConfigSettingsInherit, self).set_values()

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsInherit, self).get_values()
        config_parameter = self.env['ir.config_parameter'].sudo()
        is_multi_user = config_parameter.get_param('activities_management_app.is_multi_user')
        data_table_all_activity = config_parameter.get_param('activities_management_app.data_table_all_activity')
        data_table_plan_activity = config_parameter.get_param('activities_management_app.data_table_plan_activity')
        data_table_overdue_activity = config_parameter.get_param(
            'activities_management_app.data_table_overdue_activity')
        data_table_today_activity = config_parameter.get_param('activities_management_app.data_table_today_activity')
        data_table_done_activity = config_parameter.get_param('activities_management_app.data_table_done_activity')
        data_table_cancel_activity = config_parameter.get_param('activities_management_app.data_table_cancel_activity')

        counter_plan_activity = config_parameter.get_param('activities_management_app.counter_plan_activity')
        counter_all_activity = config_parameter.get_param('activities_management_app.counter_all_activity')
        counter_overdue_activity = config_parameter.get_param('activities_management_app.counter_overdue_activity')
        counter_today_activity = config_parameter.get_param('activities_management_app.counter_today_activity')
        counter_done_activity = config_parameter.get_param('activities_management_app.counter_done_activity')
        counter_cancel_activity = config_parameter.get_param('activities_management_app.counter_cancel_activity')

        res.update(is_multi_user=is_multi_user or False)
        res.update(data_table_all_activity=data_table_all_activity or False)
        res.update(data_table_plan_activity=data_table_plan_activity or False)
        res.update(data_table_overdue_activity=data_table_overdue_activity or False)
        res.update(data_table_today_activity=data_table_today_activity or False)
        res.update(data_table_done_activity=data_table_done_activity or False)
        res.update(data_table_cancel_activity=data_table_cancel_activity or False)

        res.update(counter_all_activity=counter_all_activity or False)
        res.update(counter_plan_activity=counter_plan_activity or False)
        res.update(counter_overdue_activity=counter_overdue_activity or False)
        res.update(counter_today_activity=counter_today_activity or False)
        res.update(counter_done_activity=counter_done_activity or False)
        res.update(counter_cancel_activity=counter_cancel_activity or False)
        return res




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
