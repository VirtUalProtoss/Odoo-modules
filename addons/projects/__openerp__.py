# -*- coding: utf-8 -*-
{
    'name': "Проекты",
    'summary': """
        Управление проектами""",
    'description': """
        Управление проектами.
    """,
    'author': "MGLife",
    'website': "http://www.mglife.ru",
    'category': 'Uncategorized',
    'version': '0.0.1',
    'depends': ['base', 'hr'],
    'application': True,
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'data/mglife.xml',
    ],
}
