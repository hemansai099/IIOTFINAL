# 🎛️ IIoT Smart Factory Pipeline — **Group 4**

<p align="center">
  <img src="https://img.shields.io/badge/IIoT-Smart%20Factory-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/MQTT-Mosquitto-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Edge-Computing-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Cloud-MongoDB-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Dashboard-Streamlit-pink?style=for-the-badge" />
</p>

<p align="center">
  <i>An end-to-end Industrial IoT system integrating simulated machines, MQTT communication, Raspberry Pi edge processing, cloud database storage, and a neon-themed real-time monitoring dashboard.</i>
</p>

---

# 🚀 Project Overview

This project implements a **full-scale IIoT architecture** that mirrors real industrial smart factory systems. It demonstrates the complete flow of data from **machines → edge node → cloud → operator dashboard**, supporting:

- Real-time telemetry  
- Edge analytics  
- Cloud storage  
- Machine command control  
- Visualization & diagnostics  

The system is modular, scalable, and structured to align with modern **Industry 4.0** architectures.

---

# 🎯 Project Objectives

### ✔ Build a fully operational IIoT data pipeline  
### ✔ Simulate realistic industrial multi-sensor telemetry  
### ✔ Perform edge-level alerting & data filtering  
### ✔ Store historical data in MongoDB  
### ✔ Provide a neon-themed operator dashboard (Streamlit HMI)  
### ✔ Enable two-way MQTT control (START / STOP)  
### ✔ Implement a system health monitor for diagnostics  

---

# 🏗️ System Architecture

```
SIMULATED MACHINES (Laptop)
        │
        ▼
LOCAL MQTT BROKER (Raspberry Pi)
        │
        ▼
EDGE NODE (Raspberry Pi)
  - SQLite Logging
  - Threshold Alerts
  - Data Cleansing & Forwarding
        │
        ▼
CLOUD MQTT BROKER (Laptop)
        │
        ▼
MongoDB Cloud Database
        │
        ▼
Neon Streamlit Dashboard (Laptop)
```

### **Architecture Layers**

| Layer | Description |
|-------|-------------|
| **Physical Device Layer** | Four simulated machines generating industrial telemetry |
| **Network Layer** | MQTT pub/sub communication |
| **Edge Layer (Pi)** | Cleansing, SQLite logging, alert detection, forward to cloud |
| **Cloud Layer** | Mosquitto + MongoDB storage |
| **Application Layer** | Real-time HMI Dashboard + analytics |

---

# 🧰 Technologies Used

| Layer | Technology | Function |
|------|------------|----------|
| Physical Devices | Python Simulator | Sensor data generation |
| Communication | MQTT (Mosquitto) | Telemetry + command messaging |
| Edge Processing | Raspberry Pi | Filtering, SQLite, alerts, forwarding |
| Cloud Database | MongoDB | Long-term telemetry storage |
| Application Layer | Streamlit | Interactive operator dashboard |

---

# 📁 Repository Structure

```
├── sim_machines_cmd.py      # Machine telemetry simulator
├── edge.py                  # Edge analytics node (Raspberry Pi)
├── dashboard_app.py         # Neon UI Streamlit Dashboard
├── images/                  # Architecture diagrams, dashboard screenshots
└── README.md                # Project documentation
```

---

# 🏭 1. Physical Device Layer – Machine Simulator

The `sim_machines_cmd.py` script simulates **4 industrial machines**, each generating:

- 🌡️ Temperature (25–90°C)  
- 📳 Vibration (0.1–2.5 g)  
- ⚡ Motor Current (2–10 A)  
- 🔄 RPM (900–3000)  

### Sensor Topic Format  
```
factory/machineX/sensors
```

### Command Topic  
```
factory/machineX/cmd
```

### Sample Payload  
```json
{
  "timestamp": 1764605530.1184,
  "temperature": 67.51,
  "vibration": 0.11,
  "motor_current": 9.51,
  "rpm": 1284
}
```

---

# 📡 2. Network Layer – MQTT Messaging

MQTT was selected because it is:

✔ Lightweight  
✔ Perfect for low-latency industrial communication  
✔ Supports bi-directional control  
✔ Industry-standard protocol in IIoT  

---

# 🖥️ 3. Edge Layer – Raspberry Pi

The **smart edge gateway** (`edge.py`) performs:

### 🔍 Real-Time Alert Detection  
Thresholds:

| Parameter | Threshold |
|----------|-----------|
| Temperature | > 85°C |
| Vibration | > 2.0 g |
| Current | > 9 A |

### 💾 Local SQLite Logging  
### 🧹 Data Cleansing & Forwarding  
### ☁️ MongoDB Upload  

---

# ☁️ 4. Cloud Layer – MQTT + MongoDB

### **Cloud MQTT Broker**
Running on laptop, handling:

- Upstream telemetry  
- Alerts  
- Operator commands  

### **MongoDB Database**
Stores two collections:

- `sensor_data`  
- `alerts`  

Each document includes:

- machine ID  
- timestamp  
- temperature  
- vibration  
- motor current  
- rpm  
- alert metadata  

---

# 🎛️ 5. Application Layer – Streamlit Neon Dashboard

The operator HMI provides:

### 🏠 Home Dashboard
- Live machine cards  
- Alerts preview  
- START/STOP machine controls  

### 📈 Analytics  
- Sensor trends over time  

### 📄 Reports  
- Downloadable CSVs  
- Tabular sensor & alert data  

### 🛠 Diagnostics  
- FFT vibration analysis  
- RPM histograms  
- Heatmaps & machine timelines  

### 🧪 System Health  
- MQTT broker check  
- MongoDB connectivity  
- Packet delay  
- Sensor lag  

---

# ▶️ Running the System

### 1️⃣ Start MQTT Broker  
```
mosquitto -c "C:\Program Files\mosquitto\mosquitto.conf"
```

### 2️⃣ Start Machine Simulator  
```
python sim_machines_cmd.py
```

### 3️⃣ Run Edge Node  
```
python3 edge.py
```

### 4️⃣ Launch Dashboard  
```
streamlit run dashboard_app.py
```

Open at: **http://localhost:8501**

---

# 🏆 Results

- Fully functional multi-layer IIoT architecture  
- Real-time monitoring dashboard  
- Stable two-way MQTT control  
- Edge + cloud separation following industrial design  

---

# ⚠️ Challenges

- MQTT port conflicts  
- Timestamp inconsistencies  
- Windows Mosquitto binding issues  
- Dashboard refresh lag  

---

# 🔮 Future Improvements

- Predictive maintenance ML models  
- Real hardware sensor integration  
- Dockerized deployment  
- OPC-UA support  
- Cloud-native IoT (AWS/GCP)

---

# 👨‍🎓 Authors

**Group 4 – MFG 598: Industrial Internet of Things  
Arizona State University**
