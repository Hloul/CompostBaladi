from odoo import http
from odoo.http import request


class ActivityBackend(http.Controller):

    @http.route('/activities_management/fetch_dashboard_data', type="json", auth='user')
    def fetch_dashboard_data(self):
        user_id = request.env.user
        print("aCTIVITY bAC")
        activity_ids = request.env['mail.activity'].search([('user_id', '=', user_id.id)])
        total_count = request.env['mail.activity'].search_count([('user_id', '=', user_id.id)])
        print(total_count,'ddddddddddddddddd')
        # data_table_all_activity = request.env['res.config.settings'].search([('data_table_all_activity', '=', user_id.id)])

        data_table_all_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.data_table_all_activity')
        data_table_done_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.data_table_done_activity')
        data_table_plan_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.data_table_plan_activity')
        data_table_today_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.data_table_today_activity')
        data_table_overdue_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.data_table_overdue_activity')
        data_table_cancel_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.data_table_cancel_activity')

        counter_all_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.counter_all_activity')
        counter_overdue_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.counter_overdue_activity')
        counter_today_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.counter_today_activity')
        counter_plan_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.counter_plan_activity')
        counter_done_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.counter_done_activity')
        counter_cancel_activity = request.env['ir.config_parameter'].sudo().get_param('activities_management_app.counter_cancel_activity')


        print("data_table_all_activity",data_table_all_activity)
        overdue = request.env['mail.activity'].search_count(
            [('state', '=', 'overdue'), ('user_id', '=', user_id.id)])

        planned = request.env['mail.activity'].search_count(
            [('state', '=', 'planned'), ('user_id', '=', user_id.id)])

        done = request.env['mail.activity'].search_count(
            [('state', '=', 'done'), ('user_id', '=', user_id.id)])

        cancel = request.env['mail.activity'].search_count(
            [('state', '=', 'cancel'), ('user_id', '=', user_id.id)])

        today = request.env['mail.activity'].search_count(
            [('state', '=', 'today'), ('user_id', '=', user_id.id)])

        dashboard_data = {}
        # user_id = request.env.user
        # ticket_data = {}
        # users = {}
        # res_users = request.env['res.users'].search([])
        # for user in res_users:
        #     users[user.id] = user.name

        # dashboard_data['users'] = users
        dashboard_data['user_id'] = user_id.name
        activity = []
        order_count = []
        count = {}
        for datas in activity_ids:
            order_data = {}
            order_count.append(datas.id)
            order_data['res_name'] = datas.res_name
            order_data['type'] = datas.activity_type_id.name if datas.activity_type_id.name else ""
            order_data['supervisor'] = datas.supervisor_id.name if datas.supervisor_id.name else ""
            order_data['date_deadline'] = datas.date_deadline
            order_data['user_id'] = datas.user_id.name if datas.user_id.name else ""
            order_data['date_done'] = datas.date_done
            order_data['feedback'] = datas.feedback
            order_data['state'] = datas.state
            order_data['summary'] = datas.summary
            activity.append(order_data)
            # data[datas.stage_id.name] = order
        dashboard_data['activity'] = activity
        dashboard_data['total_count'] = total_count
        dashboard_data['overdue'] = overdue
        dashboard_data['done'] = done
        dashboard_data['planned'] = planned
        dashboard_data['cancel'] = cancel
        dashboard_data['today'] = today
        dashboard_data['data_table_all_activity'] = data_table_all_activity
        dashboard_data['data_table_done_activity'] = data_table_done_activity
        dashboard_data['data_table_plan_activity'] = data_table_plan_activity
        dashboard_data['data_table_today_activity'] = data_table_today_activity
        dashboard_data['data_table_overdue_activity'] = data_table_overdue_activity
        dashboard_data['data_table_cancel_activity'] = data_table_cancel_activity

        dashboard_data['counter_all_activity'] = counter_all_activity
        dashboard_data['counter_overdue_activity'] = counter_overdue_activity
        dashboard_data['counter_today_activity'] = counter_today_activity
        dashboard_data['counter_plan_activity'] = counter_plan_activity
        dashboard_data['counter_done_activity'] = counter_done_activity
        dashboard_data['counter_cancel_activity'] = counter_cancel_activity
        return dashboard_data
