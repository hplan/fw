#!/usr/bin/env python
__metaclass__ = type
import DatabaseHelper as helper
import Product as pdo
import Bz as bzo


class DatabaseExecutor:

    def __init__(self):
        self.db = helper.DatabaseHelper()
        pass

    def create_db(self):
        self.db.create()

    def bz_query(self):
        sql = "select id, bz_name, bz_pwd, bz_host, bz_token from bz;"
        (conn, cursor) = self.db.query(sql)
        try:
            bz = bzo.Bz()
            for row in cursor:
                bz.set("id", row[0])
                bz.set("bz_name", row[1])
                bz.set("bz_pwd", row[2])
                bz.set("bz_host", row[3])
                bz.set("bz_token", row[4])
            return bz
        finally:
            conn.close()

    def bz_add(self, bz):
        if 'bz_name' not in bz and 'bz_host' not in bz and 'bz_pwd' not in bz:
            raise Exception("IllegalArgument product %s " % bz)
        sql = "INSERT INTO bz(bz_name, bz_host, bz_pwd) VALUES ('%s', '%s', '%s')" \
              % (bz['bz_name'], bz['bz_host'], bz['bz_pwd'])
        self.db.insert(sql)

    def bz_update(self, bz):
        sql_template = "UPDATE bz set '%s' = '%s'"
        for key in bz.keys():
            sql = sql_template % (key, bz[key])
            self.db.update(sql)

    def prod_add(self, product):
        if 'name' not in product and 'alias' not in product and 'dir' not in product:
            raise Exception("IllegalArgument product %s " % product)

        sql = "INSERT INTO product(name, alias, dir) VALUES ('%s', '%s', '%s')" \
              % (product['name'], product['alias'], product['dir'])
        self.db.insert(sql)

    def prod_update(self, product, rid):
        sql_template = "UPDATE product set '%s' = '%s' where id = %d"
        for key in product.keys():
            sql = sql_template % (key, product[key], rid)
            self.db.update(sql)

    def prod_delete(self, rid):
        sql = "delete from product where id = %d" % rid
        self.db.delete(sql)

    def prod_query(self):
        sql = "select id, name, alias, dir, prev_tag from product;"
        (conn, cursor) = self.db.query(sql)
        try:
            pds = []
            for row in cursor:
                product = pdo.Product()
                product.set("id", row[0])
                product.set("name", row[1])
                product.set("alias", row[2])
                product.set("dir", row[3])
                product.set("prev_tag", row[4])
                pds.append(product)
            return pds
        finally:
            conn.close()

    def get_product(self, rid):
        sql = "select id, name, alias, dir, prev_tag from product where id=%d;" % rid
        (conn, cursor) = self.db.query(sql)
        try:
            for row in cursor:
                product = pdo.Product()
                product.set("id", row[0])
                product.set("name", row[1])
                product.set("alias", row[2])
                product.set("dir", row[3])
                product.set("prev_tag", row[4])
                return product
        finally:
            conn.close()
