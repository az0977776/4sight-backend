#!/usr/bin/python

import sqlite3


class SQLConnection:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def clear_database(self):
        self.conn.execute("drop table if exists area;")
        self.conn.execute("drop table if exists feed;")
        self.conn.execute("drop table if exists count;")
        self.conn.execute("drop table if exists prediction;")

    def close(self):
        self.conn.close()

    def init_database(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS area
            (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name varchar(128) NOT NULL
            );'''
        )

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS feed
            (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name varchar(128) NOT NULL,
                url varchar(128) NOT NULL,
                a_id INTEGER NOT NULL,
                FOREIGN KEY (a_id) REFERENCES area(id)
            );'''
        )

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS count
            (
                f_id INTEGER NOT NULL,
                time TIMESTAMP NOT NULL,
                count INTEGER NOT NULL,
                FOREIGN KEY (f_id) REFERENCES feed(id)
            );'''
        )

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS prediction
            (
                f_id INTEGER NOT NULL,
                time TIMESTAMP NOT NULL,
                count INTEGER NOT NULL,
                FOREIGN KEY (f_id) REFERENCES feed(id)
            );'''
        )

    def add_area(self, id, name):
        self.conn.execute("Insert into area (id, name) values ({}, {})".format(id, name))


if __name__ == "__main__":
    s = SQLConnection("test.db")
    s.clear_database()
    s.init_database()
    s.close()