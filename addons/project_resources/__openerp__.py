# -*- coding: utf-8 -*-
{
    'name': "Ресурсы проектов",
    'summary': """
        Управление ресурсами по проектам""",
    'description': """
        Управление ресурсами - материалы, инструменты, технологии, время, работники, финансы и т.д., используемые в проектах.
    """,
    'author': "MGLife",
    'website': "http://www.mglife.ru",
    'category': 'Uncategorized',
    'version': '0.0.2',
    'depends': ['project', 'mrp'],
    'application': True,
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}