import sys
from Adafruit_IO import MQTTClient 
from pymongo import MongoClient 
from datetime import datetime, timedelta
import json
from bson import ObjectId


# Set up Adafruit MQTT
AIO_FEED_ID = "loragateway"
AIO_USERNAME = "phanAn3123"
AIO_KEY = "aio_UZXY79JgqU0wMOlt2CR5OCkJdwox"

last_save_time = None

# Set up MongoDB
client = MongoClient("localhost", 27017)
db = client.Test
collection = db.Test
collection_realtime = db.Realtime

def connected(client):
    print("Connect success ...")
    client.subscribe(AIO_FEED_ID)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe success ...")

def disconnected(client):
    print("Disconnect ...")
    sys.exit (1)

def message(client , feed_id , payload):
    global last_save_time
    
    try:
        json_data = json.loads(payload)
        date = datetime.now()
        date_atual = date.strftime("%Y-%m-%d %H:%M:%S")
        
        if last_save_time is None or (date - last_save_time) >= timedelta(minutes=1):
            data = {
                "soil": json_data['soil'],
                "time": date_atual,
                "temperature": json_data['temp'],
                "humidity": json_data['hum']
            }
            print(data)
            collection.insert_one(data)
            last_save_time = date
        else:
            query = { "_id": ObjectId("66600e9781e4e82d58f5316c") }
            new_values = { 
                "$set": {
                    "soil": json_data['soil'],
                    "temperature": json_data['temp'],
                    "humidity": json_data['hum'],
                }
            }
            collection_realtime.update_one(query, new_values)
            print(f"Realtime data updated: {new_values}")
    except json.JSONDecodeError:
        print("Don't transmit JSON.")

client = MQTTClient(AIO_USERNAME, AIO_KEY)

# Register callbacks
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

# Connect to Adafruit IO
client.connect()

# Start a background loop to handle incoming messages
client.loop_background()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stopping the script due to KeyboardInterrupt")
    client.disconnect()