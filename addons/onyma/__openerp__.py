# -*- coding: utf-8 -*-
{
    'name': "Billing Onyma",
    'summary': """
        Интеграция с Onyma""",
    'description': """
        Модуль интеграции с биллингом Onyma
    """,
    'author': "MGLife",
    'website': "http://www.mglife.ru",
    'category': 'Uncategorized',
    'version': '0.0.1',
    'depends': ['base', 'base_external_dbsource'],
    'application': True,
    'data': [
        'ir.model.access.csv',
        'views/views.xml',
        'data.xml',
    ],
}
