from flask import Flask, jsonify, request, render_template, redirect
from modules.db import DBHandler
from modules.orm import *
from datetime import datetime
from keras.models import load_model
import numpy as np
import env
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination

storage = []
app = Flask(__name__)


model = load_model(env.NEURAL_DIR)

def predict(sound: str) -> int:
    chunk = 3
    x = [int(sound[i*chunk:(i+1)*chunk], 16)/4096 for i in range(len(sound)//chunk)]
    s:np._ArrayLikeInt = model.predict([sorted(x)], verbose=0)
    return int(s.argmax())


@app.route('/')
def index():
    return render_template('index.html', users=UserInfo.get_all(), title="노인 보호 시스템")


@app.route('/user/<int:user_id>')
def user_specific(user_id):
    print(user_id)
    print(UserInfo.get(user_id))
    return render_template('user_specific.html', user=UserInfo.get(user_id), title="노인 정보")

@app.route('/get', methods=['GET'])
def get_data():
    handler = DBHandler(env.MAIN_DB_NAME)
    try:
        val = request.args.get("val")
        device_id = int(request.args.get('id'))
        if val == None or device_id == None:
            raise ValueError("the value is not valid")
        # handler.insert('sensor_data', device_id=device_id, min=db_min, max=db_max, avg=db_avg, datetime=datetime.now())
        predicted = predict(val)
        SensorData.add_sensor_val(device_id, '.', predicted)
        return jsonify({'result': 'success', 'predict': env.DATA_CLASS[predicted]})
    except Exception as e:
        return jsonify({'result': 'failed', 'error_code': str(e)})

@app.route('/add_note', methods=['POST'])
def add_note():
    data = dict(request.form)
    # user_id = int(request.args.get('user_id'))
    Description.add_note(data.get('user_id'), data.get('detail'))
    
    return redirect(f'/user/{data.get("user_id")}')









@app.route('/server-url', methods=['POST']) #고유번호
def submit_form():
    dbs = get_db()
    unique_number = request.form.get('unique-number')
    print('고유번호:', unique_number)
    users = dbs.select(UserInfo.TABLE_NAME, "*", where=f"user_id = {unique_number}")
    li = [UserInfo(*user) for user in users]
    # 여기서 unique_id 값을 데이터베이스에 저장하거나 다른 로직을 처리할 수 있습니다.
    return render_template('index.html', users=li, title="노인 보호 시스템")


@app.route('/server-url2', methods=['POST']) #이름
def submit_form2():
    dbs = get_db()
    unique_name = request.form.get('unique-name')
    print('이름:', unique_name)
    users = dbs.select(UserInfo.TABLE_NAME, "*", where=f"name = '{unique_name}'")
    li = [UserInfo(*user) for user in users]
    # 여기서 unique_id 값을 데이터베이스에 저장하거나 다른 로직을 처리할 수 있습니다.
    return render_template('index.html', users=li, title="노인 보호 시스템")

@app.route('/server-url3', methods=['POST']) #지역
def submit_form3():
    dbs = get_db()
    unique_place = request.form.get('unique-place')
    print('지역:', unique_place)
    users = dbs.select(UserInfo.TABLE_NAME, "*", where=f"place = '{unique_place}'")
    li = [UserInfo(*user) for user in users]
    # 여기서 unique_id 값을 데이터베이스에 저장하거나 다른 로직을 처리할 수 있습니다.
    return render_template('index.html', users=li, title="노인 보호 시스템")

@app.route('/server-url4', methods=['POST']) #지역
def submit_form4():
    dbs = get_db()
    unique_phone_number = request.form.get('unique-phone-number')
    print('전화번호:', unique_phone_number)
    users = dbs.select(UserInfo.TABLE_NAME, "*", where=f"phone_number = '{unique_phone_number}'")
    li = [UserInfo(*user) for user in users]
    # 여기서 unique_id 값을 데이터베이스에 저장하거나 다른 로직을 처리할 수 있습니다.
    return render_template('index.html', users=li, title="노인 보호 시스템")

@app.route('/server-url5', methods=['POST']) #지역
def submit_form5():
    dbs = get_db()
    unique_PG = request.form.get('unique-PG')
    print('관심위험등급:', unique_PG)
    users = dbs.select(UserInfo.TABLE_NAME, "*", where=f"PG = '{unique_PG}'")
    li = [UserInfo(*user) for user in users]
    # 여기서 unique_id 값을 데이터베이스에 저장하거나 다른 로직을 처리할 수 있습니다.
    return render_template('index.html', users=li, title="노인 보호 시스템")




if __name__ == "__main__":
    # dbc = DBHandler(env.MAIN_DB_NAME)
    # dbc.insert("user_info", _id_name="user_id", name="백종문", age=54, place="광주", phone_number="010-1234-5678", max = 0, PG = 0)
    # user = dbc.select_one("user_info")
    # dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=0)
    # dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=1)
    # dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=2)
    # device = dbc.select_one("beacon")
    # # dbc.insert("sensor_data", device_id=device[0], max=10, min=0, avg=5, datetime = datetime.now())
    # print(*dbc.select("user_info", order_by="user_id"), sep="\n")
    # print(*dbc.select("beacon"), sep="\n")
    app.run('0.0.0.0', port=8000)