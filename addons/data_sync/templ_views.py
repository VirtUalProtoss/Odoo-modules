# -*- coding: utf-8 -*-

template = '''
<record model="ir.actions.act_window" id="data_sync_%(name)s_action_window">
    <field name="name">%(name)s</field>
    <field name="res_model">data_sync.%(name)s</field>
    <field name="view_mode">tree,form</field>
</record>
<menuitem name="%(caption)s" id="data_sync.%(name)s" parent="data_sync.root" action="data_sync_%(name)s_action_window"/>
'''
tables = {
    'connection_rules': 'Правила подключений',
    'connections': 'Подключения',
    'objects': 'Объекты',
    'db_types': 'Типы СУБД',
    'direction_types': 'Направления',
    'object_map_links': 'Связи карт объектов',
    'object_map_rules': 'Правила карт объектов',
    'object_maps': 'Карты объектов',
    'object_types': 'Типы объектов',
    'profile_maps': 'Карты профилей',
    'profiles': 'Профили',
    'rules': 'Правила',
    'rule_types': 'Типы правил',
    'schemas': 'Схемы',
    'session_logs': 'Логи сессий',
    'sessions': 'Сессии',
    'template_parts': 'Части шаблонов',
    'templates': 'Шаблоны',
}

for tbl in tables:
    ftempl = template % ({
        'name': tbl,
        'caption': tables[tbl],
    })
    print ftempl