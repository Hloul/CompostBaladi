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

    'depends': ['base', 'account'],

    'data': [
        'views/account_move_views.xml',
    ],
}
