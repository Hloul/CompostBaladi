# -*- coding: utf-8 -*-
# Part of BAS. See LICENSE file for full copyright and licensing details.

{
    'name': 'Analytic Distribution on Stock Picking',
    'version': '16.0.0.1',
    'category': 'Warehouse',
    'summary': 'Add Analytic Distribution on Stock Picking and Stock Move',
    'description': """Adds an 
    analytic distribution in Odoo stock move and stock picking 
    """,
    'author': 'BAS',
    'website': 'https://www.bas.com',
    'depends': ['base','sale_management','stock','analytic',"stock_account",'purchase'],
    'data': [
                "views/stock_move_views.xml"
            ],
	'qweb': [ ],
    "license":'OPL-1',
    'demo': [ ],
    'test': [ ],
    'installable': True,
    'auto_install': False,
}

