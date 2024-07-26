from flask import Blueprint, render_template, jsonify, request
from pymongo import MongoClient
import json
from datetime import datetime
from Adafruit_IO import Client


AIO_FEED_ID = "button"
AIO_USERNAME = "phanAn3123"
AIO_KEY = "aio_UZXY79JgqU0wMOlt2CR5OCkJdwox"
aio = Client(AIO_USERNAME, AIO_KEY)

# Connect to Database Sensor
client = MongoClient("localhost", 27017)
db = client.Test
collection = db.Test

views = Blueprint('views', __name__)

@views.route('/test')
def test():
    cursor = collection.find()
    data_list = [{**record, '_id': str(record['_id'])} for record in cursor]
    data_time = []
    data_temp = []
    for x in data_list:
        data_time.append(x['time'])
        data_temp.append(x['temperature'])
    return jsonify(data_time,data_temp)

@views.route('/dashboard')
def overview():
    cursor = collection.find()
    data_list = [{**record, '_id': str(record['_id'])} for record in cursor]
    data_latest = data_list[-1]
    return render_template('Dashboard.html',data = data_latest)


@views.route('/weather')
def weather():
    return render_template('weather.html')

@views.route('/chart')
def chart():
    cursor = collection.find()
    labels = []
    values = []
    for record in cursor:
        record_time = datetime.strptime(record['time'], '%Y-%m-%d %H:%M:%S')
        formatted_time = record_time.strftime('%d-%m-%Y')
        labels.append(formatted_time)
        values.append(record['temperature'])
    return render_template('test.html', time = labels, temperature = values)


@views.route('/testcallback')
def testcallback():
    cursor = collection.find()
    data_list = [{**record, '_id': str(record['_id'])} for record in cursor]
    data_latest = data_list[-1]
    print(data_latest)
    data_temp = data_latest['temperature']
    return render_template('testcallback.html', data = data_latest)

@views.route('/update_button_status', methods=['GET'])
def update_button_status():
    button_value = request.args.get('value')
    aio.send(AIO_FEED_ID, button_value)
    if button_value == 'ON':
        button_text = 'OFF'
    else:
        button_text = 'ON'
    return jsonify({'button_text': button_text})

@views.route('/')
def base():
    return render_template('base.html')