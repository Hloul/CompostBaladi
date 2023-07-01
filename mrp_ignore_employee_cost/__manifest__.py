# -*- coding: utf-8 -*-
{
    'name': "mrp_ignore_employee_cost",

    'summary': """
        Ignore employee cost in manufacturing
        """,

    'description': """
        Don't consider employee hour cost in the manufacturing orders
    """,

    'author': "BAS",
    'website': "https://www.bas.sarl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['mrp'],

    # always loaded
    'data': [],
}
