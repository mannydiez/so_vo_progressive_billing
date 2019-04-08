# -*- coding: utf-8 -*- d

{
    'name': 'SO VO Progress Billing',
    'version': '1.3',
    'category': 'Sales/Accounting',
    'summary': 'User can generate customer invoice using Progress Billing % with VO Rate method from Variation Order',
    'description': "Variation Order is additional sales order/change request order. User can generate customer invoice using Progress Billing % with VO Rate method from Variation Order.",
    'author': "HashMicro/Smidh Vadera/Dev (Braincrew Apps)",
    'website':"www.hashmicro.com",
    'maintainer': 'HashMicro',
    'depends': ['so_progress_billing','account','construction_contracting_change_order'],
    'data': [
        'views/so_vo_progress_billing.xml',
        'views/so_vo_account_analytic_view.xml',
        'wizard/sale_make_invoice_advance_view.xml',
        'sequence/sequence.xml',
    ],    
    'installable': True,
    'application': False,
    'demo' : [
        'demo/module_data.xml',
        ],
    
}