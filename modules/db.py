import sqlite3 as sql
from random import randint
from datetime import datetime

def connect_db(name):
    conn = sql.connect(name, isolation_level=None)
    c = conn.cursor()
    try:
        query = """
            CREATE TABLE IF NOT EXISTS "user_info" (
                    user_id        INTEGER NOT NULL,
                    name        TEXT NOT NULL,
                    age        INTEGER NOT NULL DEFAULT 0,
                    place        TEXT NOT NULL,
                    PRIMARY KEY(user_id AUTOINCREMENT)
            )
            """
        c.execute(query)
        query = """
            CREATE TABLE IF NOT EXISTS beacon (
                    device_id        INTEGER NOT NULL,
                    user_id        INTEGER NOT NULL,
                    point        INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES user_info(user_id),
                    PRIMARY KEY(device_id AUTOINCREMENT)
            )
            """
        c.execute(query)
        query = """
            CREATE TABLE sensor_data (
                    device_id        INTEGER NOT NULL,
                    max        INTEGER NOT NULL,
                    min        INTEGER NOT NULL,
                    avg        INTEGER NOT NULL,
                    datetime   DATETIME NOT NULL,
                    FOREIGN KEY(device_id) REFERENCES beacon(device_id)
            )
            """
        c.execute(query)

        conn.commit()
        print("db initalized")
    except sql.OperationalError:
        pass
    return conn


class DBHandler:
    def __init__(self, name:str):
        self.name = name
        self.conn = connect_db(name)
        self.cur = self.conn.cursor()

    def is_free_id(self, table:str, id_name:str, number):
        return len(self.select(table, where=f"{id_name}={number}")) == 0

    def get_free_id(self, table:str, id_name:str, capacity=5):
        while True:
            num = randint(10**(capacity-1), 10**capacity-1)
            if self.is_free_id(table, id_name, num):
                return num

    def select(self, table:str, finders:tuple="*", where:str=None, order_by:str=None, reverse=False, limit:int=0):
        if type(finders) in [list, tuple]:
            finders = ", ".join(finders)
        query = f"SELECT {finders} FROM {table}"
        if where:
            query += f" WHERE {where}"
        if order_by:
            query += f" ORDER BY {order_by} {'DESC' if reverse else 'ASC'}"
        if limit > 0:
            query += f" LIMIT {limit}"

        self.cur.execute(query)
        return self.cur.fetchall()

    def select_one(self, table:str, finders="*", where=None):
        if type(finders) in [list, tuple]:
            finders = ", ".join(finders)
        query = f"SELECT {finders} FROM {table}{f' WHERE {where}' if where else ''}"
        self.cur.execute(query)
        result = self.cur.fetchone()
        if len(result) == 1:
            result = result[0]
        return result
    def insert(self, table:str, _id_name:str=None, capacity:int=5, **kwargs):
        if _id_name:
            kwargs[_id_name] = self.get_free_id(table, _id_name, capacity)
        query = f"INSERT INTO {table}({', '.join(kwargs.keys())}) values({', '.join(['?']*len(kwargs))})"
        self.cur.execute(query, tuple(kwargs.values()))
        self.conn.commit()

    def delete(self, table:str, where:str):
        query = f"DELETE FROM {table} WHERE {where}"
        self.cur.execute(query)
        self.conn.commit()

    def __repr__(self):
        tables = ", ".join(s[0] for s in self.cur.fetchall())
        return f"{self.name}({tables})"


if __name__ == "__main__":
    dbc = DBHandler("noin.db")
    dbc.insert("user_info", _id_name="user_id", name="백민재", age=15, place="강남")
    user = dbc.select_one("user_info")
    dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=0)
    dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=1)
    dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=2)
    device = dbc.select_one("beacon")
    # dbc.insert("sensor_data", device_id=device[0], max=10, min=0, avg=5, datetime = datetime.now())
    print(*dbc.select("user_info", order_by="user_id"), sep="\n")
    print(*dbc.select("beacon"), sep="\n")
    # print(*dbc.select("sensor_data"), sep="\n")
