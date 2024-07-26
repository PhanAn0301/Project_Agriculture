from flask import Blueprint, jsonify
from pymongo import MongoClient

# Connect to Database Sensor
client = MongoClient("localhost", 27017)
db = client.Test
collection = db.Realtime

callback = Blueprint('callback', __name__)

@callback.route('/')
def test():
    cursor = collection.find()
    data = [{**record, '_id': str(record['_id'])} for record in cursor]
    print(data)
    return jsonify(data)
