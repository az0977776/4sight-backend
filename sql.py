#!/usr/bin/python

import sqlite3
from datetime import datetime, timedelta

db_name = "test.db"

class SQLConnection:

    def __init__(self):
        self.conn = sqlite3.connect(db_name)

    def __del__(self):
        self.conn.close()

    def clear_database(self):
        self.conn.execute("drop table if exists area;")
        self.conn.execute("drop table if exists feed;")
        self.conn.execute("drop table if exists count;")
        self.conn.execute("drop table if exists prediction;")

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
                a_id INTEGER NOT NULL,
                time TIMESTAMP NOT NULL,
                count INTEGER NOT NULL,
                FOREIGN KEY (a_id) REFERENCES area(id)
            );'''
        )

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS prediction
            (
                a_id INTEGER NOT NULL,
                time TIMESTAMP NOT NULL,
                count INTEGER NOT NULL,
                FOREIGN KEY (a_id) REFERENCES area(id)
            );'''
        )

    def add_area(self, a_id, name):
        cur = self.conn.cursor()
        cur.execute("Insert into area(id, name) values (?, ?)", (a_id, name))
        self.conn.commit()

    def add_feed(self, f_id, name, url, a_id):
        cur = self.conn.cursor()
        cur.execute("Insert into feed(id, name, url, a_id) values (?, ?, ?, ?)", (f_id, name, url, a_id))
        self.conn.commit()

    def add_count(self, a_id, time, count):
        cur = self.conn.cursor()
        cur.execute("Insert into count(a_id, time, count) values (?, ?, ?)", (a_id, time, count))
        self.conn.commit()

    def add_prediction(self, a_id, time, count):
        cur = self.conn.cursor()
        cur.execute("Insert into prediction(a_id, time, count) values (?, ?, ?)", (a_id, time, count))
        self.conn.commit()

    def get_area_name(self, a_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM area where id=?", (str(a_id)))
        rows = cur.fetchall()
        if len(rows) == 0:
            return ""
        assert(len(rows) == 1)
        return rows[0][1]

    def get_all_area(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM area")

        rows = cur.fetchall()

        ret = []
        for r in rows:
            ret.append({
                "a_id": r[0],
                "a_name": r[1]
            })
        return {"areas": ret}

    def get_area_feeds(self, a_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM feed where a_id=?", (str(a_id),))

        rows = cur.fetchall()

        ret = []
        for r in rows:
            ret.append({
                "f_id": r[0],
                "f_name": r[1],
                "url": r[2],
            })

        return {
            "a_id": a_id,
            "a_name": self.get_area_name(a_id),
            "count": self.get_most_recent_count(a_id),
            "feeds": ret
        }       

    def get_feed(self, f_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM feed where id=?", (str(f_id),))

        rows = cur.fetchall()
        if len(rows) == 0:
            return {}
        assert(len(rows) == 1)
        feed = rows[0]

        return {
            "f_id": feed[0],
            "f_name": feed[1],
            "url": feed[2],
            "a_id": feed[3],
        }    

    def get_counts(self, a_id, time_start=None, time_end=None):
        # default interval start time is an hour ago
        if not time_start:
            time_start = datetime.now() - timedelta(hours=1)

        # default interval end time is current time
        if not time_end:
            time_end = datetime.now()

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM count where a_id=? and time between ? and ?", (str(a_id), time_start, time_end))

        rows = cur.fetchall()

        ret = []
        for r in rows:
            ret.append([r[1], r[2]])
        return {
            "a_id": a_id,
            "a_name": self.get_area_name(a_id),
            "counts": ret
        }

    def get_most_recent_count(self, a_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM count where a_id=? ORDER BY datetime(time) DESC LIMIT 1", (str(a_id)))

        rows = cur.fetchall()
        if len(rows) == 0:
            return 0
        return rows[0][2]

    def get_predictions(self, a_id, time_start=None, time_end=None):
        # default interval start time is now
        if not time_start:
            time_start = datetime.now()

        # default interval end time is an hour in the future
        if not time_end:
            time_end = datetime.now() + timedelta(hours=1)

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM prediction where a_id=? and time between ? and ?", (str(a_id), time_start, time_end))

        rows = cur.fetchall()
        ret = []
        for r in rows:
            ret.append([r[1], r[2]])
        return {
            "a_id": a_id,
            "a_name": self.get_area_name(a_id),
            "prediction": ret
        }

if __name__ == "__main__":
    videos = [
        [0, "food_court", "http://32.208.120.218/mjpg/video.mjpg", 0],
        [1, "laundromat", "http://81.14.37.24:8080/mjpg/video.mjpg", 0],
        [2, "shops", "http://87.139.9.247/mjpg/video.mjpg", 0],
        [3, "hair_salon", "http://220.240.123.205/mjpg/video.mjpg", 0],
        [4, "town_park", "http://89.29.108.38/mjpg/video.mjpg", 0],
        [5, "time_square", "http://166.130.18.45:1024/mjpg/video.mjpg", 0]
    ]

    s = SQLConnection()
    s.clear_database()
    s.init_database()

    # populating the test.db with some dummy values
    s.add_area(0, "general_testing")
    for v in videos:
        s.add_feed(v[0], v[1], v[2], v[3])

    for i in range(10):
        s.add_count(0, datetime.now() - timedelta(minutes=i * 15), 3 + i)
        s.add_prediction(0, datetime.now() +  timedelta(minutes=i * 15), 20 + i)

    print(s.get_counts(0, datetime.now() - timedelta(days=1)))
    print(s.get_predictions(0, time_end=datetime.now() + timedelta(days=1)))
