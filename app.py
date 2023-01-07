from flask import Flask, jsonify, request
import json
from datetime import datetime
storage = []

app = Flask(__name__)
@app.route('/get' ,methods=['GET'])
def get_data():
    db_counter = int(request.args.get('db_counter'))
    category = request.args.get('category')
    storage.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "db_counter": db_counter, "category": category})
    return jsonify({'result':'success', 'msg': storage})

@app.route('/search', methods=['GET'])
def ave_get():
    db_avg = 0
    cnt = 0
    category = request.args.get('category')
    for i in storage:
        print(i)
        if i['category'] == category:
            db_avg += i['db_counter']
            cnt += 1
    if cnt != 0:
        db_avg/=cnt
    return jsonify({'result':'success', 'msg': db_avg})



if __name__ == "__main__":
    app.run('0.0.0.0', port=80)