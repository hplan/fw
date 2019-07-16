#!/usr/bin/env python
__metaclass__ = type
import sqlite3


class DatabaseHelper:

    def __init__(self):
        self.db = "./db/fw.db"

    def create(self):
        conn = sqlite3.connect(self.db)
        try:
            db = conn.cursor()
            db.execute('''
            CREATE TABLE IF NOT EXISTS bz(
            id        INTEGER      PRIMARY KEY AUTOINCREMENT,
            bz_name   TEXT  NOT NULL,
            bz_pwd    TEXT  NOT NULL,
            bz_host   TEXT  NOT NULL,
            bz_token  TEXT
            )
            ''')
            db.execute('''
            CREATE TABLE IF NOT EXISTS product(
            id        INTEGER      PRIMARY KEY AUTOINCREMENT,
            name      TEXT  NOT NULL,
            alias     TEXT  NOT NULL,
            dir       TEXT  NOT NULL,
            prev_tag  TEXT
            )
            ''')
            # only when bz was empty, initial one
            # cursor = db.execute("select id from bz")
            # r = cursor.fetchall()
            # if len(r) == 0:
            #     db.execute("INSERT INTO bz(bz_name, bz_pwd, bz_host) VALUES ('', '', '')")
            conn.commit()
        except Exception as e:
            print "*** Something went wrong ***"
            print e.message
        finally:
            conn.close()

    def query(self, sql):
        conn = sqlite3.connect(self.db)
        try:
            db = conn.cursor()
            cursor = db.execute(sql)
            return conn, cursor
        finally:
            pass

    def cud(self, sql):
        conn = sqlite3.connect(self.db)
        try:
            db = conn.cursor()
            db.execute(sql)
            conn.commit()
        except Exception as e:
            raise e
        finally:
            conn.close()

    def insert(self, sql):
        self.cud(sql)

    def delete(self, sql):
        self.cud(sql)

    def update(self, sql):
        self.cud(sql)
