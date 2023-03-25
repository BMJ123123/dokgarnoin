from modules.db import DBHandler
from modules.orm import *
import env

if __name__ == '__main__':
    datas = [
        ['백민욱', '강북', '010-0000-2222', 22],
        ['백종문', '강북', '010-0000-2222', 54],
        ['백민재', '강북', '010-0000-2222', 20],
    ]
    dbc = DBHandler(env.MAIN_DB_NAME)
    for name, place, phone, age in datas:
        dbc.insert("user_info", _id_name="user_id", name=name,
                   age=age, place=place,  phone_number=phone)
        user = dbc.select_one("user_info")
        for p in range(3):
            dbc.insert("beacon", _id_name="device_id",
                       capacity=6, user_id=user[0], point=0)

    # dbc.insert("sensor_data", device_id=device[0], max=10, min=0, avg=5, datetime = datetime.now())
    print(*dbc.select("user_info", order_by="user_id"), sep="\n")
    print(*dbc.select("beacon"), sep="\n")
