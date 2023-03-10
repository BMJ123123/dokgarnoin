from flask import Flask, jsonify, request
from modules.db import DBHandler
from modules.orm import *
from datetime import datetime
storage = []
app = Flask(__name__)
@app.route('/get', methods=['GET'])
def get_data():
    handler = DBHandler("noin.db")
    try:
        val = request.args.get("val")
        device_id = int(request.args.get('id'))
        if val == None or device_id == None:
            raise ValueError("the value is not valid")
        # handler.insert('sensor_data', device_id=device_id, min=db_min, max=db_max, avg=db_avg, datetime=datetime.now())
        Beacon.get(device_id).add_sensor_val(val)
        return jsonify({'result': 'success'})
    except Exception as e:
        return jsonify({'result': 'failed', 'error_code': str(e)})


@app.route('/search', methods=['GET'])
def ave_get():
    device_id = request.args.get('id')
    val = 0
    # cnt = 0
    # category = request.args.get('category')
    # for i in storage:
    #     print(i)
    #     if i['category'] == category:
    #         db_avg += i['db_counter']
    #         cnt += 1
    # if cnt != 0:
    #     db_avg /= cnt 17:38:00
    # handler = DBHandler("noin.db") 
    # db_avg = handler.select_one("sensor_data", finders=("avg(avg)",), where=f"device_id={device_id}")
    return jsonify({'result': 'success', 'msg': val})


if __name__ == "__main__":
    app.run('0.0.0.0', port=8000)
