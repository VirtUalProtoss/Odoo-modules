# -*- coding: utf-8 -*-
{
    'name': "Группы",
    'summary': """
        Управление группами""",
    'description': """
        Управление группами.
    """,
    'author': "MGLife",
    'website': "http://www.mglife.ru",
    'category': 'Uncategorized',
    'version': '0.0.1',
    'depends': ['base', 'hr'],
    'application': True,
    'installable': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        #'data/mglife.xml',
    ],
}
