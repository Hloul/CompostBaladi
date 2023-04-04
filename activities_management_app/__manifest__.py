{

    'name': 'All in one Activities Management',
    'author': 'Edge Technologies',
    'version': '16.0.1.0',
    'live_test_url':'https://youtu.be/wP_SpqSDaCk',
    "license" : "OPL-1",
    "images":['static/description/main_screenshot.png'],
    'category': 'Extra Tools',
    'summary': 'All In One Schedule Activities all in one Activity Management Activity Dashboard Advance Schedule Activity Management Dashboard Activities Dashboard all Activities Management advance activity management all on one Schedule activity advance activities',
    'description': "All In One Schedule Activities , Activity Dashboard , Advance Schedule Activity , Dynamic Action For Multiple Activities,Done and cancel state for activity,Dynamic state changes in activity,Multi user activity,My Activity supervisor activity and all activity",
    'depends': [
        'base','mail',
    ],
    'data': [
        'security/ir.model.access.csv',
    	'security/security.xml',
    	'views/inherited_mail_activity_view.xml',
        'views/activity_tag.xml',
        'views/res_config_settings.xml',
        'wizard/activity_feedback_wizard_view.xml',
        'wizard/activity_cancel_wizard_view.xml',



    ],
    # 'qweb' : [],

    'assets': {
        'web.assets_frontend': [
            ],
        'web.assets_backend': [
            'activities_management_app/static/src/js/dashboard_view.js',
            'activities_management_app/static/src/css/custom.css',
            'activities_management_app/static/src/xml/base.xml',
            ],
        'web._assets_common_scripts': [
        ],
        # 'web.assets_qweb': [
        #     'vehicle_rental_management_app/static/src/xml/base.xml',
        # ],
        },

    'demo': [],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 35,
    'currency': "EUR",
}
