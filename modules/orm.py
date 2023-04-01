from modules.db import DBHandler
import env
from abc import *
from datetime import datetime, timedelta


def get_db() -> DBHandler:
    return DBHandler(env.MAIN_DB_NAME)

# UserInfo 클래스는 사용자 정보를 나타내는 클래스
class UserInfo:
    TABLE_NAME = "user_info"

    def __init__(self, user_id, name, age, place, phone_number, PG):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.place = place
        self.phone_number = phone_number
        self.PG = PG

    def __repr__(self) -> str:
        return f"UserInfo_{self.user_id}(name={self.name}, age={self.age}, place={self.place})"

    def get_beacons(self) -> list:
        dbs = get_db()
        many = dbs.select(Beacon.TABLE_NAME, where=f"user_id={self.user_id}")
        return [Beacon(*one) for one in many]
    #사용자와 연관된 Beacon 인스턴스를 모두 반환

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
    # 모든 사용자 정보를 반환

    @staticmethod
    def add(name: str, age: int, place: str):
        dbs = get_db()
        many = dbs.select()
    # 사용자 정보를 추가

    def get_note(self):
        return Description.get_all(self.user_id)
    # 사용자와 연관된 Description 인스턴스를 모두 반환

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
    # get_point 메서드는 point 값을 인식 가능한 문자열로 반환

    @staticmethod
    def get(device_id: int):
        dbs = get_db()
        one = dbs.select_one(Beacon.TABLE_NAME, where=f"{device_id=}")
        if one is None:
            return None
        return Beacon(*one)
    # 특정 비콘 정보를 반환
    
    def get_env_desc(self):
        dbs = get_db()
        now_time = datetime.now()
        time_divisions = [timedelta(hours=24), timedelta(hours=23), timedelta(hours=22), timedelta(hours=21), timedelta(hours=20), timedelta(hours=19), timedelta(hours=18), timedelta(hours=17), timedelta(hours=16), timedelta(hours=15), timedelta(hours=14), timedelta(hours=13), timedelta(hours=12), timedelta(hours=11), timedelta(hours=10), timedelta(hours=9), timedelta(hours=8), timedelta(hours=7), timedelta(hours=6), timedelta(hours=5), timedelta(hours=4), timedelta(hours=3), timedelta(hours=2), timedelta(hours=1)]
        time_series = [now_time - times for times in time_divisions] + [now_time]
        format_time = "%Y-%m-%d %H:%M"
        # print(query)
        outputs = []
        for num in range(len(time_series)-1):
            query = f"device_id='{self.device_id}' AND datetime BETWEEN '{time_series[num].strftime(format_time)}' AND '{time_series[num+1].strftime(format_time)}'"
                                #여기에 따음표 붙임
            
            many = dbs.select(SensorData.TABLE_NAME, where=query, order_by="datetime", reverse=True)
            many = [SensorData(*one) for one in many]
            sounds = [0] * 3
            for one in many:
                sounds[one.sound_type] += 1
            outputs.append([time_series[num].strftime("%H:%M")] + sounds)
        return outputs
    # 비콘의 소리 정보를 최근 24시간 동안 시간 단위로 반환
            
    def get_env_1_week_desc(self):
            dbs = get_db()
            now_time = datetime.now()
            time_division = timedelta(days=7)
            timerange = now_time - time_division
            format_time = "%Y-%m-%d %H:%M"
            # print(query)
            query = f"device_id={self.device_id} AND datetime BETWEEN '{timerange.strftime(format_time)}' AND '{now_time.strftime(format_time)}'"
            many = dbs.select(SensorData.TABLE_NAME, where=query, order_by="datetime", reverse=True)
            many = [SensorData(*one) for one in many]
            sounds = [0] * 3
            for one in many:
                sounds[one.sound_type] += 1
            return sounds
    # 비콘의 소리 정보를 최근 1주일 동안 반환
            
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
    # 비콘의 소리 정보를 모두 반환
    
    @staticmethod
    def get_all():
        dbs = get_db()
        many = dbs.select(Beacon.TABLE_NAME)
        return [Beacon(*one) for one in many]
    # 유저에 대입되는 모든 비콘 정보를 반환

    @staticmethod
    def add(user_id: int, point: int):
        dbs = get_db()
        many = dbs.select()

    def add_sensor_val(self, val: str, sound_type: int):
        dbs = get_db()
        dbs.insert(SensorData.TABLE_NAME, device_id=self.device_id,
                   str_value=val, sound_type=sound_type, datetime=datetime.now())
    # 센서 값을 추가하는 방법

class SensorData(DBHandler):
    TABLE_NAME = "sensor_data"
    SILENT = 0
    MIDDLE = 1
    NOISE = 2

    def __init__(self, device_id: int, str_value: str, date: datetime, sound_type: int):
        self.device_id = device_id
        self.value_str = str_value
        self.datetime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
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
    def __init__(self, note_number:int, user_id: int, note_detail: str, date: datetime):
        self.note_number = note_number
        self.user_id = user_id
        self.note_detail = note_detail
        self.datetime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    
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

    @staticmethod
    def delete_note(note_number: int):
        dbs = get_db()
        dbs.delete(Description.TABLE_NAME, where=f"{note_number=}")
    # @staticmethod
    # def print_note(user_id: int, note_detail: str):
    #     dbs = get_db()
    #     many = dbs.select(Description.TABLE_NAME)
    #     return [Description(*one) for one in many]



if __name__ == "__main__":
    user = UserInfo.get(191899)
    print(user)
