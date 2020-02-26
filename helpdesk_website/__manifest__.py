# -*- coding: utf-8 -*-
{
    'name': "helpdesk_website",

    'summary': """
        Helpdesk Frontend Static web (Build from ReactJS)""",

    'description': """
        This module is helpdesk ticket reporting app that using Odoo11 Restful API for managing database. 
    """,

    'author': "Blueseas Enterprise",
    'website': "http://www.blueseas.co.th",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}