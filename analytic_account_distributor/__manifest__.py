# -*- coding: utf-8 -*-
# Part of BAS. See LICENSE file for full copyright and licensing details.

{
    'name': "Analytic Account Distributor",

    'summary': """
        Distribute Analytic Account to all lines in the account move
        """,

    'description': """
        Distribute Analytic Account to all lines in the account move
    """,

    'author': "Mohamed ElGhiriany",

    'category': 'Accounting/Accounting',
    'version': '1.0',
    "license":'OPL-1',
    'depends': ['base', 'account'],

    'data': [
        'views/account_move_views.xml',
    ],
}
