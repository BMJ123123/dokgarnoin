from modules.db import DBHandler
import env
from abc import *
from datetime import datetime
def get_db() -> DBHandler:
    return DBHandler(env.MAIN_DB_NAME)

class UserInfo:
    TABLE_NAME = "user_info"
    def __init__(self, user_id, name, age, place):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.place = place

    def __repr__(self) -> str:
        return f"UserInfo_{self.user_id}(name={self.name}, age={self.age}, place={self.place})"

    @staticmethod
    def get(user_id):
        dbs = get_db()
        one = dbs.select_one(UserInfo.TABLE_NAME, where=user_id)
        return UserInfo(*one)
    
    @staticmethod
    def add(name, age, place):
        dbs = get_db()
        many = dbs.select()

class Beacon(DBHandler):
    TABLE_NAME = "beacon"
    BOTTOM = 0
    RIGHT = 1
    TOP = 2

    def __init__(self, device_id, user_id, point):
        self.device_id = device_id
        self.user_id = user_id
        self.point = point
        
    def __repr__(self) -> str:
       return f"Beacon_{self.device_id}(user_id={self.user_id}, point={self.get_point()})"

    def get_point(self):
        if self.point == Beacon.BOTTOM:
            return "BOTTOM"
        elif self.point == Beacon.RIGHT:
            return "RIGHT"
        elif self.point == Beacon.TOP:
            return "TOP"
        return "UNKNOWN"
    @staticmethod
    def get(device_id):
       dbs = get_db()
       one = dbs.select_one(Beacon.TABLE_NAME, where=device_id)
       return Beacon(*one)

    @staticmethod
    def add(user_id, point):
       dbs = get_db()
       many = dbs.select()

    def add_sensor_val(self, _max, _min ,avg):
        dbs = get_db()
        dbs.insert(SensorData.TABLE_NAME, device_id= self.device_id, max=_max, min=_min, avg=avg, datetime=datetime.now())

class SensorData(DBHandler):
    TABLE_NAME = "sensor_data"
    def __init__(self, device_id, _max, _min, avg, datetime, valtype):
        self.device_id = device_id
        self.max = _max
        self.min = _min
        self.avg = avg
        self.datetime = datetime
        self.type = valtype
        
    def __repr__(self) -> str:
        return f"SensorData_{self.device_id}(_max={self.max}, _min={self.min}, datetime={self.datetime})"

    @staticmethod
    def get(device_id):
        dbs = get_db()
        many = dbs.select(SensorData.TABLE_NAME, where=device_id)
        return [SensorData(*one) for one in many]
    
    @staticmethod
    def get_by_type(valtype):
        dbs = get_db()
        many = dbs.select(SensorData.TABLE_NAME, where=f"type={valtype}")
        return [SensorData(*one) for one in many]


if __name__ == "__main__":
    user = UserInfo.get(43130)
    print(user)