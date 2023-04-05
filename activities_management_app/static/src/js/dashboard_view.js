odoo.define('activities_management_app.Dashboard',function(require){
"use strict";

var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
//var Dialog = require('web.Dialog');
//var field_utils = require('web.field_utils');
var session = require('web.session');
//var web_client = require('web.web_client');
var Widget = require('web.Widget');
var rpc = require('web.rpc');
const { getBundle, loadBundle } = require('@web/core/assets');

var _t = core._t;
var QWeb = core.qweb;

var Dashboard = AbstractAction.extend({
	hasControlPanel: true,
	contentTemplate: 'activities_management_app.Dashboard',
	events: {
	    'click .zoom': 'on_click_list',
//	    'click .card-view': 'on_click_list',
	    'change .stage_name': 'on_click_list',
		'click .column': 'on_click_list',
		'click .form_view' : 'on_click_form',
	},

	init: function(parent, context) {

		this._super(parent, context);
		this.dashboard_stage_templates = ['activities_management_app.dashboard_view'];
//		this.dashboard_order_templates = ['activities_management_app.orders'];
	},
	willStart: function() {
		var self = this;
		return $.when(loadBundle(this), this._super()).then(function() {
			return self.fetch_data();
		})
	},

	start: function() {
		var self = this;
		self.render_dashboards();
		return this._super();
	},

	fetch_data: function() {
		var self = this;
		var prom = this._rpc({
			route: '/activities_management/fetch_dashboard_data',
		});

		prom.then(function(result) {
			self.data = result['activity'];
			self.count = result['total_count']
			self.overdue = result['overdue']
			self.planned = result['planned']
			self.done = result['done']
			self.user_id = result['user_id']
			self.cancel = result['cancel']
			self.today = result['today']

			self.data_table_all_activity = result['data_table_all_activity']
			self.data_table_done_activity = result['data_table_done_activity']
			self.data_table_plan_activity = result['data_table_plan_activity']
			self.data_table_today_activity = result['data_table_today_activity']
			self.data_table_overdue_activity = result['data_table_overdue_activity']
			self.data_table_cancel_activity = result['data_table_cancel_activity']

			self.counter_all_activity = result['counter_all_activity']
			self.counter_overdue_activity = result['counter_overdue_activity']
			self.counter_today_activity = result['counter_today_activity']
			self.counter_plan_activity = result['counter_plan_activity']
			self.counter_done_activity = result['counter_done_activity']
			self.counter_cancel_activity = result['counter_cancel_activity']
		});
		return prom;
	},

	render_dashboards: function() {
		var self = this;
		_.each(this.dashboard_stage_templates, function(template) {
			self.$('.o_dashboard_stage').append(QWeb.render(template, {widget: self}));
		});
	},

	on_click_list: function (ev){
		var self = this;
		var model_name = $(ev.currentTarget).find('.name').text();
		var model = '';
		var name = '';
		var stage_name;
		var user = session.uid
		var model_view = '';
		var state = '';
		var $link = $('.zoom');
		if (ev.currentTarget.firstElementChild && ev.currentTarget.firstElementChild.firstElementChild){
			stage_name = ev.currentTarget.firstElementChild.firstElementChild.innerText;
		}
        state = stage_name.toLowerCase();
        name = 'Activity';

        if ($.trim(state) == 'all'){
            self.do_action({
                name: name,
                views: [[false, 'list'], [false, 'form']],
                domain: [["user_id", "=", user]],
                res_model: 'mail.activity',
                type: 'ir.actions.act_window',
                target: 'current',
            });

           }

        else{
                self.do_action({
                name: name,
                views: [[false, 'list'], [false, 'form']],
                domain: [["user_id", "=", user],['state', '=', $.trim(state)]],
                res_model: 'mail.activity',
                type: 'ir.actions.act_window',
                target: 'current',
                });
            }
	},

//	on_click_form: function(ev){
//		var self = this;
//		var model_name = $(ev.currentTarget).prev().prev().text();
//		var model = '';
//		var name = '';
//		var model_view = '';
//        name = 'Vehicle Rental Contract';
//        model = 'vehicle.rental.contract';
//        model_view = 'activities_management_app.vehicle_rental_contract_view_form';
//		self.do_action({
//			name: name,
//			views: [[false, 'form']],
//			res_model: model_name,
//			type: 'ir.actions.act_window',
//			target: 'current',
//		});
//	},

});

core.action_registry.add('activities_management_dashboard', Dashboard);

return Dashboard;
});