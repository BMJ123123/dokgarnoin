from modules.db import DBHandler
import env
from abc import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def get_db() -> DBHandler:
    return DBHandler(env.MAIN_DB_NAME)


class UserInfo:
    TABLE_NAME = "user_info"

    def __init__(self, user_id, name, age, place, phone_number, max, PG):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.place = place
        self.phone_number = phone_number
        self.max = max
        self.PG = PG

    def __repr__(self) -> str:
        return f"UserInfo_{self.user_id}(name={self.name}, age={self.age}, place={self.place})"

    def get_beacons(self) -> list:
        dbs = get_db()
        many = dbs.select(Beacon.TABLE_NAME, where=f"user_id={self.user_id}")
        return [Beacon(*one) for one in many]

    @staticmethod
    def get(user_id):
        dbs = get_db()
        one = dbs.select_one(UserInfo.TABLE_NAME, where=f"{user_id=}")
        return UserInfo(*one)

    @staticmethod
    def get_all():
        dbs = get_db()
        users = dbs.select(UserInfo.TABLE_NAME)
        return [UserInfo(*user) for user in users]

    @staticmethod
    def add(name: str, age: int, place: str):
        dbs = get_db()
        many = dbs.select()

    # @staticmethod
    # def get_unique():
    #     dbs = get_db()
    #     users = dbs.select(UserInfo.TABLE_NAME, where=f"{user_id=}")


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
    def get(device_id: int):
        dbs = get_db()
        one = dbs.select_one(Beacon.TABLE_NAME, where=f"{device_id=}")
        if one is None:
            return None
        return Beacon(*one)
    
    def get_env_desc(self):
        dbs = get_db()
        now_time = datetime.now()
        time_divisions = [timedelta(hours=24), timedelta(hours=23), timedelta(hours=22), timedelta(hours=21), timedelta(hours=20), timedelta(hours=19), timedelta(hours=18), timedelta(hours=17), timedelta(hours=16), timedelta(hours=15), timedelta(hours=14), timedelta(hours=13), timedelta(hours=12), timedelta(hours=11), timedelta(hours=10), timedelta(hours=9), timedelta(hours=8), timedelta(hours=7), timedelta(hours=6), timedelta(hours=5), timedelta(hours=4), timedelta(hours=3), timedelta(hours=2), timedelta(hours=1)]
        time_series =  [now_time - times for times in time_divisions]
        format_time = "%Y-%m-%d %H:%M"
        # print(query)
        outputs = []
        for series in time_series:
            query = f"device_id='{self.device_id}' AND datetime BETWEEN '{series.strftime(format_time)}' AND '{now_time.strftime(format_time)}'"
                                #여기에 따음표 붙임
            
            many = dbs.select(SensorData.TABLE_NAME, where=query, order_by="datetime", reverse=True)
            many = [SensorData(*one) for one in many]
            sounds = [0] * 3
            for one in many:
                sounds[one.sound_type] += 1
            outputs.append([series.strftime("%H:%M")] + sounds)
        return outputs
            
    def get_env_1_week_desc(self):
            dbs = get_db()
            now_time = datetime.now()
            time_divisions = [timedelta(hours=168)]
            time_series =  [now_time - times for times in time_divisions]
            format_time = "%Y-%m-%d %H:%M"
            # print(query)
            outputs = []
            for series in time_series:
                query = f"device_id={self.device_id} AND datetime BETWEEN '{series.strftime(format_time)}' AND '{now_time.strftime(format_time)}'"
                many = dbs.select(SensorData.TABLE_NAME, where=query, order_by="datetime", reverse=True)
                many = [SensorData(*one) for one in many]
                sounds = [0] * 3
                for one in many:
                    sounds[one.sound_type] += 1
                outputs.append([series.strftime("%H:%M")] + sounds)
            return outputs
            
    def get_env_total(self):
        dbs = get_db()
        now_time = datetime.now()
        time_divisions = [timedelta(hours=1)]
        time_series = [now_time - times for times in time_divisions]
        format_time = "%Y-%m-%d %H:%M"
        outputs = []
        total_sounds = [0] * 3 # 3개의 sound_type에 해당하는 값을 모두 더하기 위한 리스트
        for series in time_series:
            query = f"device_id={self.device_id} AND datetime BETWEEN '{series.strftime(format_time)}' AND '{now_time.strftime(format_time)}'"
            many = dbs.select(SensorData.TABLE_NAME, where=query, order_by="datetime", reverse=True)
            many = [SensorData(*one) for one in many]
            for one in many:
                total_sounds[one.sound_type] += 1 # 각각의 sound_type에 해당하는 값을 모두 더함
            outputs.append([series.strftime("%H:%M")] + total_sounds)
        return outputs
    
    @staticmethod
    def get_all():
        dbs = get_db()
        many = dbs.select(Beacon.TABLE_NAME)
        return [Beacon(*one) for one in many]

    @staticmethod
    def add(user_id: int, point: int):
        dbs = get_db()
        many = dbs.select()

    def add_sensor_val(self, val: str, sound_type: int):
        dbs = get_db()
        dbs.insert(SensorData.TABLE_NAME, device_id=self.device_id,
                   str_value=val, sound_type=sound_type, datetime=datetime.now())


class SensorData(DBHandler):
    TABLE_NAME = "sensor_data"
    SILENT = 0
    MIDDLE = 1
    NOISE = 2

    def __init__(self, device_id: int, str_value: str, datetime: datetime, sound_type: int):
        self.device_id = device_id
        self.value_str = str_value
        self.datetime = datetime
        self.sound_type = sound_type

    def __repr__(self) -> str:
        return f"SensorData_{self.device_id}({self.value_str=}, datetime={self.datetime}, sound_type={self.sound_type})"

    def decode_audio(self, chunk: int = 3):
        return [int(self.value_str[i*chunk:(i+1)*chunk], 16) for i in range(len(self.value_str)//chunk)]

    @staticmethod
    def get(device_id: int) -> list:
        dbs = get_db()
        many = dbs.select(SensorData.TABLE_NAME, where=f"{device_id=}", order_by="datetime", reverse=True)
        return [SensorData(*one) for one in many]
    @staticmethod
    def add_sensor_val(device_id, val: str, sound_type: int):
        dbs = get_db()
        dbs.insert(SensorData.TABLE_NAME, device_id=device_id,
                   str_value=val, sound_type=sound_type, datetime=datetime.now())
        
class Description(DBHandler):
    TABLE_NAME = "description"
    def __init__(self, note_number:int, user_id: int, note_detail: str, datetime: datetime):
        self.note_number = note_number
        self.user_id = user_id
        self.note_detail = note_detail
        self.datetime = datetime
    
    def __repr__(self):
        return f"Description_{self.note_number}(user_id={self.user_id}, {self.note_detail=}, datetime={self.datetime})"
    @staticmethod
    def get(note_number:int):
        dbs = get_db()
        one = dbs.select_one(Description.TABLE_NAME, where=f"{note_number=}")
        return one

    @staticmethod
    def get_all(user_id: int):
        dbs = get_db()
        many = dbs.select(Description.TABLE_NAME, where=f"{user_id=}")
        return [Description(*one) for one in many]
    
    @staticmethod
    def add_note(user_id: int, note_detail: str):
        dbs = get_db()
        dbs.insert(Description.TABLE_NAME, user_id=user_id, note_detail=note_detail, datetime=datetime.now(), _id_name="note_number")

    # @staticmethod
    # def print_note(user_id: int, note_detail: str):
    #     dbs = get_db()
    #     many = dbs.select(Description.TABLE_NAME)
    #     return [Description(*one) for one in many]



if __name__ == "__main__":
    user = UserInfo.get(191899)
    print(user)
