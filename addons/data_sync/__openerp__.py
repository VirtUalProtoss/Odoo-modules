# -*- coding: utf-8 -*-
{
    'name': "Data Syncer",
    'summary': """
        Синхронизация данных между СУБД""",
    'description': """
        Синхронизация данных между СУБД
    """,
    'author': "MGLife",
    'website': "http://www.mglife.ru",
    'category': 'Uncategorized',
    'version': '0.0.1',
    'depends': ['base', 'base_external_dbsource'],
    'application': True,
    'data': [
        #'ir.model.access.csv',
        'views/views.xml',
        'data/data.xml',
    ],
}
