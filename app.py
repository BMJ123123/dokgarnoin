from flask import Flask, jsonify, request, render_template, redirect
from modules.db import DBHandler
from modules.orm import *
from datetime import datetime
from keras.models import load_model
import numpy as np
import env
# from flask_sqlalchemy import SQLAlchemy
# from flask_paginate import Pagination

storage = []
app = Flask(__name__, static_url_path='/static')


model = load_model(env.NEURAL_DIR)


def predict(sound: str) -> int:
    chunk = 3
    x = [int(sound[i*chunk:(i+1)*chunk], 16) /
         4096 for i in range(len(sound)//chunk)]
    s: np._ArrayLikeInt = model.predict([sorted(x)], verbose=0)
    return int(s.argmax())



@app.route('/')
def main():
    return render_template('index.html', users=UserInfo.get_all(), title="노인 보호 시스템", trees=['Dashboard'])

@app.route('/about/vision')
def about():
    return render_template('vision.html', title="노인 보호 시스템", trees=['Dashboard', 'vison'])

@app.route('/contact')
def contact():
    return render_template('contact.html', title="노인 보호 시스템", trees=['Dashboard', 'Contact'])


@app.route('/user')
def user_specific():
    user_id = int(request.args.get('user_id'))
    user = UserInfo.get(user_id)
    return render_template('user_specific.html', user=user, title="노인 정보", trees=['Dashboard', user.name])


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

@app.route('/user/graph')
def get_data_graph():
    user_id = int(request.args.get('user_id'))
    user = UserInfo.get(user_id)
    datas = user.get_beacons()
    pie = []
    for i, data in enumerate(datas):
        data:Beacon = data.get_env_desc()
        one_pie = data.get_env_1_week_desc()
        for k in range(3):
            pie[k] = one_pie[k]
        labels = [d[0] for d in data]
        datasets = [
            {
                "label": 'silent',
                "data": [d[1] for d in data],
                "borderColor": "#66b3ff",
                "fill": False,
                "borderWidth": 1.6,
                "tension": 0.4,
                "pointStyle": False,
            },
            {
                "label": 'netural',
                "data": [d[2] for d in data],
                "borderColor": "#ff6666",
                "fill": False,
                "borderWidth": 1.6,
                "tension": 0.4,
                "pointStyle": False
            },
            {
                "label": 'noisy',
                "data": [d[3] for d in data],
                "borderColor": "#ffa500",
                "fill": False,
                "borderWidth": 1.6,
                "tension": 0.4,
                "pointStyle": False
            },
        ]
        datas[i] = dict(labels=labels, datasets=datasets)
    pie_chart = {
        "data": {
            "datasets": [{
                "data": pie,
                "backgroundColor": ['#66b3ff', '#ff9999', '#ffa500'],
                # "hoverBackgroundColor": ['#ffff99', '#ff6666', '#4d94ff'],
            }],
            "labels": ['silent', 'netural', 'noisy'],  # 각 카테고리 이름
        },
        "options": {
            "title": {
                "display": True,
                "text": "일주일 요약" # <---------------------------------------------------------
            },
            "plugins": {
                "legend": {
                    "position": "right",  # 범례 위치 설정
                    "labels": {
                        "usePointStyle": True  # 각 항목에 포인트 스타일 사용
                    }
                }
            }
        },
        "type": "pie"  # 차트 타입
    }
    return jsonify(dict(datas=datas, pie=pie_chart))


@app.route('/notes/add', methods=['POST'])
def add_note():
    data = dict(request.form)
    print(data)
    # user_id = int(request.args.get('user_id'))
    Description.add_note(data.get('user_id'), data.get('detail'))

    return redirect(f'/user?user_id={data.get("user_id")}')


@app.route('/notes/delete', methods=['POST'])
def delete_note():
    try:
        data = request.json
        # user_id = int(request.args.get('user_id'))
        Description.delete_note(data.get('note_id'))
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'error_code': str(e)})
    return jsonify({'ok': True})


@app.route('/server-url', methods=['POST'])  # 고유번호
def submit_form():
    dbs = get_db()
    unique_number = request.form.get('unique-number')
    print('고유번호:', unique_number)
    users = dbs.select(UserInfo.TABLE_NAME, "*",
                       where=f"user_id LIKE \"%{unique_number}%\"")
    li = [UserInfo(*user) for user in users]
    # 여기서 unique_id 값을 데이터베이스에 저장하거나 다른 로직을 처리할 수 있습니다.
    return render_template('index.html', users=li, title="노인 보호 시스템")


@app.route('/server-url2', methods=['POST'])  # 이름
def submit_form2():
    dbs = get_db()
    unique_name = request.form.get('unique-name')
    print('이름:', unique_name)
    users = dbs.select(UserInfo.TABLE_NAME, "*",
                       where=f"name LIKE \"%{unique_name}%\"")
    li = [UserInfo(*user) for user in users]
    # 여기서 unique_id 값을 데이터베이스에 저장하거나 다른 로직을 처리할 수 있습니다.
    return render_template('index.html', users=li, title="노인 보호 시스템")


@app.route('/server-url3', methods=['POST'])  # 지역
def submit_form3():
    dbs = get_db()
    unique_place = request.form.get('unique-place')
    print('지역:', unique_place)
    users = dbs.select(UserInfo.TABLE_NAME, "*",
                       where=f"place LIKE \"%{unique_place}%\"")
    li = [UserInfo(*user) for user in users]
    # 여기서 unique_id 값을 데이터베이스에 저장하거나 다른 로직을 처리할 수 있습니다.
    return render_template('index.html', users=li, title="노인 보호 시스템")


@app.route('/server-url4', methods=['POST'])  # 지역
def submit_form4():
    dbs = get_db()
    unique_phone_number = request.form.get('unique-phone-number')
    print('전화번호:', unique_phone_number)
    users = dbs.select(UserInfo.TABLE_NAME, "*",
                       where=f"phone_number LIKE \"%{unique_phone_number}%\"")
    li = [UserInfo(*user) for user in users]
    # 여기서 unique_id 값을 데이터베이스에 저장하거나 다른 로직을 처리할 수 있습니다.
    return render_template('index.html', users=li, title="노인 보호 시스템")

if __name__ == "__main__":
    # dbc = DBHandler(env.MAIN_DB_NAME)
    # dbc.insert("user_info", _id_name="user_id", name="백종문", age=84, place="말레이시아", phone_number="010-1577-1577")
    # user = dbc.select_one("user_info")
    # dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=0)
    # dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=1)
    # dbc.insert("beacon",_id_name="device_id", capacity=6, user_id=user[0], point=2)
    # device = dbc.select_one("beacon")
    # # dbc.insert("sensor_data", device_id=device[0], max=10, min=0, avg=5, datetime = datetime.now())
    # print(*dbc.select("user_info", order_by="user_id"), sep="\n")
    # print(*dbc.select("beacon"), sep="\n")
    app.run('0.0.0.0', port=8000, debug=env.DEBUG)
