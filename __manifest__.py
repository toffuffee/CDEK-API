# -*- coding: utf-8 -*-
{
    'name': "cdek",
    'summary': "cdek",
    'description': "cdek",
    'author': "Paul Orlov",
    'website': "http://www.yourcompany.com",
    
    'category': 'Base',
    'version': '0.1',
    'sequence' : 2,

    'depends': ['crm','sale',"delivery"],

    'data': [
        'security/ir.model.access.csv',
        'wizard/call_courier.xml',
        'views/views.xml',
        'data/delivery_data.xml',
        'static/xml/view.xml',
        'static/xml/sale_order_inherit.xml',
        'static/xml/sale_report.xml',
        'static/xml/product_property.xml',
        'static/site/main_page.xml',
        'static/site/website_form.xml',
    ],
    'qweb': ["static/xml/*.xml"],

    'installable':True,
    'application':True,
    'auto_install':False,

    'assets': {
        'web.assets_frontend': [
            'cdek/static/styles/main.scss',
        ]
    }
}
