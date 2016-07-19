# -*- coding: utf-8 -*-
{
    'name': "Ресурсы",
    'summary': """
        Управление ресурсами""",
    'description': """
        Управление ресурсами - материалы, инструменты, технологии, время, работники, финансы и т.д.
    """,
    'author': "MGLife",
    'website': "http://www.mglife.ru",
    'category': 'Uncategorized',
    'version': '0.0.1',
    'depends': [],
    'application': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/property_types.xml',
        'data/properties.xml',
        'data/categories.xml',
        'data/resource_templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}