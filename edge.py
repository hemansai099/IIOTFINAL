import sqlite3
import json
import ssl
import time
from urllib.parse import quote_plus

import paho.mqtt.client as mqtt
from pymongo import MongoClient

DB_FILE = "machine_data.db"

# ================================================================
# 0) MONGODB ATLAS (Cloud DB)
# ================================================================
MONGO_HOST = "10.117.162.51"
MONGO_PORT =27017

try:
    
    print("[MONGO] Connecting to Laptop" )
    mongo_client=MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
    
    db = mongo_client["iiot_cloud"]
    collection_sensors = db["sensor_data"]
    collection_alerts = db["alerts"]
    
    print("[Mongo] Connected to laptop MongoDB successfully!")
    

except Exception as e:
    print("[MONGO] Failed to connect to Laptop MongoDB:", e)
  
    collection_sensors = None
    collection_alerts = None
# ================================================================
# 1) CREATE MACHINE TABLES (SQLite)
# ================================================================
def create_table_if_needed(table_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            temperature REAL,
            vibration REAL,
            motor_current REAL,
            rpm INTEGER
        );
        """
    )
    conn.commit()
    conn.close()


# ================================================================
# 2) ALERTS TABLE (SQLite)
# ================================================================
ALERTS_TABLE = "alerts"

def create_alerts_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {ALERTS_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine TEXT,
            timestamp REAL,
            alert_type TEXT,
            value REAL
        );
        """
    )
    conn.commit()
    conn.close()

create_alerts_table()

# ================================================================
# 3) THRESHOLD CHECK + PUSH ALERTS TO MONGO
# ================================================================
def check_thresholds(machine, payload):
    alerts = []

    if payload["temperature"] > 85:
        alerts.append(("High Temperature", payload["temperature"]))

    if payload["vibration"] > 2.0:
        alerts.append(("High Vibration", payload["vibration"]))

    if payload["motor_current"] > 9:
        alerts.append(("Overload Current", payload["motor_current"]))

    if not alerts:
        return

    # ---- Save in SQLite ----
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for alert_type, value in alerts:
        c.execute(
            f"""
            INSERT INTO {ALERTS_TABLE} (machine, timestamp, alert_type, value)
            VALUES (?, ?, ?, ?)
            """,
            (machine, payload["timestamp"], alert_type, value),
        )
    conn.commit()
    conn.close()

    print(f"[ALERT] {machine}: {alerts}")

    # ---- Save alerts in MongoDB ----
    if collection_alerts is not None:
        try:
            docs = []
            for alert_type, value in alerts:
                docs.append(
                    {
                        "machine": machine,
                        "timestamp": payload["timestamp"],
                        "alert_type": alert_type,
                        "value": value,
                    }
                )
            collection_alerts.insert_many(docs)
            print("[MONGO] Alerts inserted into MongoDB Atlas.")
        except Exception as e:
            print("[MONGO] Failed to insert alerts:", e)

# ================================================================
# 4) MQTT MESSAGE HANDLER
# ================================================================
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode())
    machine_id = topic.split("/")[1]

    # ---- SQLite ----
    create_table_if_needed(machine_id)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        f"""
        INSERT INTO {machine_id}
        (timestamp, temperature, vibration, motor_current, rpm)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            payload["timestamp"],
            payload["temperature"],
            payload["vibration"],
            payload["motor_current"],
            payload["rpm"],
        ),
    )
    conn.commit()
    conn.close()

    print(f"[LOCAL SAVE] {machine_id}: {payload}")

    # ---- Alerts ----
    check_thresholds(machine_id, payload)

    # ---- Forward to laptop MQTT ----
    try:
        cloud_client.publish(topic, msg.payload)
        print(f"[LAPTOP MQTT] Sent → {topic}")
    except Exception as e:
        print("[LAPTOP MQTT] Failed:", e)

    # ---- Push to MongoDB Atlas ----
    if collection_sensors is not None:
        try:
            doc = {
                "machine": machine_id,
                "timestamp": payload["timestamp"],
                "temperature": payload["temperature"],
                "vibration": payload["vibration"],
                "motor_current": payload["motor_current"],
                "rpm": payload["rpm"],
            }
            collection_sensors.insert_one(doc)
            print("[MONGO] Sensor data inserted!")
        except Exception as e:
            print("[MONGO] Failed inserting sensor doc:", e)

# ================================================================
# 5) LOCAL MQTT (Mosquitto on Pi)
# ================================================================
LOCAL_BROKER = "localhost"
client = mqtt.Client()
client.on_message = on_message
client.connect(LOCAL_BROKER)
client.subscribe("factory/+/sensors")

# ================================================================
# 6) CLOUD MQTT ON LAPTOP (Works)
# ================================================================
CLOUD_HOST = "10.117.162.51"
CLOUD_PORT = 1883

cloud_client = mqtt.Client()
try:
    cloud_client.connect(CLOUD_HOST, CLOUD_PORT)
    print(f"[LAPTOP MQTT] Connected at {CLOUD_HOST}:{CLOUD_PORT}")
except Exception as e:
    print("[LAPTOP MQTT] Connection failed:", e)

# ================================================================
# 7) RUN BOTH LOOPS
# ================================================================
print("\nEdge node running (SQLite + Laptop MQTT + MongoDB )...\n")

client.loop_start()
cloud_client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
    client.loop_stop()
    cloud_client.loop_stop()