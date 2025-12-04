# sim_machines_cmd.py  (run this on the Pi)
import json
import time
import random
import paho.mqtt.client as mqtt

BROKER = "10.117.162.70"
BASE_TOPIC = "factory"

MACHINES = ["machine1", "machine2", "machine3","machine4"]

# machine running status
machine_state = {m: True for m in MACHINES}


# ---------- MQTT callbacks ----------

def on_connect(client, userdata, flags, rc):
    print("[SIM] Connected to local broker with rc =", rc)
    # listen for commands for all machines
    client.subscribe(f"{BASE_TOPIC}/+/cmd")
    print(f"[SIM] Subscribed to {BASE_TOPIC}/+/cmd")

def on_message(client, userdata, msg):
    global machine_state
    topic = msg.topic  # factory/machine1/cmd
    try:
        payload = json.loads(msg.payload.decode())
    except Exception:
        print("[SIM] Bad JSON on", topic, "→", msg.payload)
        return

    parts = topic.split("/")
    if len(parts) < 3:
        return
    machine_id = parts[1]
    cmd = payload.get("command", "").lower()

    if machine_id in machine_state and cmd in ("start", "stop"):
        machine_state[machine_id] = (cmd == "start")
        print(f"[SIM] Command for {machine_id}: {cmd.upper()} → running={machine_state[machine_id]}")
    else:
        print("[SIM] Unknown command:", topic, payload)


# ---------- helper to make fake sensor data ----------

def make_sensor_payload():
    # You can tweak these ranges to look nicer
    return {
        "timestamp": time.time(),
        "temperature": round(random.uniform(25, 90), 2),
        "vibration": round(random.uniform(0.1, 2.5), 2),
        "motor_current": round(random.uniform(2, 10), 2),
        "rpm": random.randint(900, 3000),
    }


# ---------- main ----------

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_start()

print("[SIM] Machine publisher with START/STOP control is running...")

try:
    while True:
        for m in MACHINES:
            if machine_state[m]:
                payload = make_sensor_payload()
                topic = f"{BASE_TOPIC}/{m}/sensors"
                client.publish(topic, json.dumps(payload))
                # print(f"[SIM] Published {m}: {payload}")
        time.sleep(3.0)  # 3 Hz per machine
except KeyboardInterrupt:
    print("\n[SIM] Stopping...")
finally:
    client.loop_stop()
    client.disconnect()
