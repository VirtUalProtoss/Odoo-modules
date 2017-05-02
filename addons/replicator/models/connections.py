# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ReplicatorConnections(models.Model):
    _name = 'replicator.connections'

    name = fields.Char()
    ext_dbsource_id = fields.Many2one('base.external.dbsource', selected=True)

    @api.one
    def exec_query(self, conn, sqlquery, sqlparams, metadata=False):
        rows, cols = list(), list()
        if self.ext_dbsource_id.connector in ["sqlite", "mysql", "mssql"]:
            # using sqlalchemy
            cur = conn.execute(sqlquery, sqlparams)
            if metadata:
                cols = cur.keys()
            rows = [r for r in cur]
        else:
            # using other db connectors
            cur = conn.cursor()
            cur.execute(sqlquery, sqlparams)
            if metadata:
                cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
        if metadata:
            return{'cols': cols, 'rows': rows}
        else:
            return rows

    @api.one
    def auth(self, conn, username=None, password=None):
        sql = '''
            begin api_dog.auth(:login, :password); commit; exception when others then rollback; end;
        '''
        params = {
            'login': 's.sobolevskiy',
            'password': 'NjgZYX3J',
        }
        cur = conn.cursor()
        cur.execute(sql, params)
        #result = self.exec_query(conn, sql, params, metadata=False)
        #return result

    @api.multi
    def getTables(self):
        conn_id = self.ext_dbsource_id.id
        conn = self.ext_dbsource_id.conn_open(conn_id)
        self.auth(conn)
        sql = '''
            SELECT table_name FROM all_tables -- where view_name like ('API_%')
        '''
        params = {}
        result = self.exec_query(conn, sql, params, metadata=False)
        for row in result:
            print type(row), row
