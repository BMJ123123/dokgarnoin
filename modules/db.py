import sqlite3 as sql
from random import randint
from datetime import datetime
import env

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
                    phone_number TEXT NOT NULL,
                    PG	INTEGER,
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
            CREATE TABLE IF NOT EXISTS sensor_data (
                    device_id        INTEGER NOT NULL,
                    str_value        TEXT NOT NULL,
                    datetime   DATETIME NOT NULL,
                    sound_type INTEGER, 
                    FOREIGN KEY(device_id) REFERENCES beacon(device_id)
            )
            """
        c.execute(query)
        query = """
            CREATE TABLE IF NOT EXISTS description (
                    note_number         INTEGER NOT NULL,
                    user_id             INTEGER NOT NULL,
                    note_detail         TEXT NOT NULL,
                    datetime   DATETIME NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES user_info(user_id)
                    PRIMARY KEY(note_number AUTOINCREMENT)
            )
            """
        c.execute(query)

        conn.commit()
        # print("db initalized")
    except sql.OperationalError as err:
        print(err)
        pass
    return conn


class DBHandler:
    def __init__(self, name:str):
        self.name = name
        self.conn = connect_db(name)
        self.cur = self.conn.cursor()

    def is_free_id(self, table:str, id_name:str, number):
        return len(self.select(table, where=f"{id_name}={number}")) == 0
    # 특정 테이블에서 특정 ID필드 값이 중복되지 않는지 확인하는 함수

    def get_free_id(self, table:str, id_name:str, capacity=5): # 
        while True:
            num = randint(10**(capacity-1), 10**capacity-1)
            if self.is_free_id(table, id_name, num):
                return num
    # 특정 테이블에서 사용 가능한 ID값을 생성하는 함수

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
        # print(query)
        self.cur.execute(query)
        return self.cur.fetchall()
    # 특정 테이블에서 데이터를 조회하는 함수 해당 조건에 맞는 데이터를 조회하고 반환함

    def select_one(self, table:str, finders="*", where=None):
        if type(finders) in [list, tuple]:
            finders = ", ".join(finders)
        query = f"SELECT {finders} FROM {table}{f' WHERE {where}' if where else ''}"
        self.cur.execute(query)
        result = self.cur.fetchone()
        if len(result) == 1:
            result = result[0]
        return result
    # 특정 테이블에서 단일 데이터를 조회하는 함수 조건에 맞는 데이터 중 첫 번째 데이터를 조회

    def insert(self, table:str, _id_name:str=None, capacity:int=5, **kwargs):
        if _id_name:
            kwargs[_id_name] = self.get_free_id(table, _id_name, capacity)
        query = f"INSERT INTO {table}({', '.join(kwargs.keys())}) values({', '.join(['?']*len(kwargs))})"
        self.cur.execute(query, tuple(kwargs.values()))
        self.conn.commit()
    # 특정 테이블에 데이터를 삽입하는 함수        

    def delete(self, table:str, where:str):
        query = f"DELETE FROM {table} WHERE {where}"
        self.cur.execute(query)
        self.conn.commit()
    # 특정 테이블에서 데이터를 삭제하는 함수 조건에 맞는 데이터를 삭제

    def __repr__(self):
        tables = ", ".join(s[0] for s in self.cur.fetchall())
        return f"{self.name}({tables})"
    #DBHandler 객체를 출력할 때 호출되며, 객체에 연결된 테이블 이름을 문자열로 반환

if __name__ == "__main__":
    dbc = DBHandler(env.MAIN_DB_NAME)
    dbc.insert("user_info", _id_name="user_id", name="백민재", age=15, place="강남", phone_number="010-1234-5678", PG=0)
    user = dbc.select_one("user_info")
    dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=0)
    dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=1)
    dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=2)
    device = dbc.select_one("beacon")
    # dbc.insert("sensor_data", device_id=device[0], max=10, min=0, avg=5, datetime = datetime.now())
    print(*dbc.select("user_info", order_by="user_id"), sep="\n")
    print(*dbc.select("beacon"), sep="\n")
    # print(*dbc.select("sensor_data"), sep="\n")
