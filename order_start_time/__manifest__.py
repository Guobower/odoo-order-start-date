# -*- coding: utf-8 -*-
{
    'name': "Order Start Time",

    'summary': """
        Order Start Time module""",

    'description': """
        This module adds start time field for each line in quotations and invoices
    """,

    'author': "Kusuma Ruslan",
    'website': "http://www.wangsamas.com",

    'category': 'Sales',
    'version': '0.1',

    'depends': ['sale_management'],

    'data': [
        'views/product.xml',
        'views/account_invoice.xml',
        'views/account_move.xml',
        'views/sale_order.xml',
    ],

}
