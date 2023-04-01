from modules.db import DBHandler
from modules.orm import *
import env

if __name__ == '__main__':
    datas = [
        ['백민욱', '강북', '010-1234-5678', 22],
        ['백종문', '광주', '010-1313-1313', 54],
        ['백민재', '서울', '010-0000-0000', 19],
        ['이찬환', '서울', '010-5566-5566', 73],
        ['서동우', '말레이시아', '010-1577-1577', 84],
    ]
    dbc = DBHandler(env.MAIN_DB_NAME)
    for name, place, phone, age in datas:
        dbc.insert("user_info", _id_name="user_id", name=name,
                   age=age, place=place,  phone_number=phone)
    users = dbc.select("user_info")
    for user in users:
        for p in range(3):
            dbc.insert("beacon", _id_name="device_id",
                        capacity=6, user_id=user[0], point=0)

    # dbc.insert("sensor_data", device_id=device[0], max=10, min=0, avg=5, datetime = datetime.now())
    print(*dbc.select("user_info", order_by="user_id"), sep="\n")
    print(*dbc.select("beacon"), sep="\n")
