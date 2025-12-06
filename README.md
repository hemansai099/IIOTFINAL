# 📦 **IIoT Smart Factory Pipeline — Group 4** ### *End-to-End Industrial IoT System with Edge Processing, Cloud Database, MQTT Messaging & Neon Dashboard* --- ## 🚀 **Project Overview** This project demonstrates a **complete Industrial IoT (IIoT) architecture**, integrating: * Simulated industrial machines * MQTT messaging for telemetry + control * Raspberry Pi edge computing * MongoDB cloud database * Real-time Streamlit Neon HMI dashboard * System diagnostics, analytics, and alerting The solution mimics an actual factory environment, showing how sensor data flows from devices → edge → cloud → application layer with full bi-directional control. --- ## 🎯 **Objectives** * Build a **fully functional IIoT data pipeline** * Generate realistic multi-sensor industrial telemetry * Perform **edge-level analytics & alert detection** * Store historical data in a cloud database * Visualize factory operations using a **real-time neon dashboard** * Implement **START/STOP** machine commands over MQTT * Validate system performance using a **System Health Monitor** --- ## 🏗 **System Architecture**
SIMULATED MACHINES 
        │
        ▼
LOCAL MQTT BROKER (Pi)
        │
        ▼
EDGE NODE (Pi)
 - SQLite Logging
 - Threshold Alerts
 - Forward Clean Telemetry
        │
        ▼
CLOUD MQTT BROKER (Laptop)
        │
        ▼
MongoDB (Laptop Cloud DB)
        │
        ▼
Streamlit Neon Dashboard (Laptop)
### Layers Included: 1. **Physical Device Layer** – Machine simulator with 4 virtual machines 2. **Network Layer** – MQTT messaging (publish/subscribe) 3. **Edge Layer** – Raspberry Pi for processing, alerts & forwarding 4. **Cloud Layer** – MongoDB + Mosquitto broker (Laptop) 5. **Application Layer** – Real-time neon dashboard --- ## 🔧 **Components & Technologies** | Layer | Technology | Role | | ---------------- | ---------------- | -------------------------------------- | | Physical Devices | Python Simulator | Generate temp, vibration, current, rpm | | Communication | MQTT (Mosquitto) | Low-latency pub/sub messaging | | Edge | Raspberry Pi | Filtering, SQLite, alerts, forwarding | | Cloud | MongoDB | Store sensor + alert data | | Application | Streamlit | HMI dashboard with real-time analytics | --- ## 📁 **Repository Structure**
├── sim_machines_cmd.py        # Machine simulator (publishes sensor data)
├── edge.py                    # Edge computing node running on Raspberry Pi
├── dashboard_app.py           # Neon Streamlit Dashboard (HMI)
├── README.md                  # Documentation
└── images/                    # Architecture diagrams + screenshots
--- ## 🏭 **1. Physical Device Layer** File: **sim_machines_cmd.py** Simulates 4 industrial machines generating: * Temperature (25–90°C) * Vibration (0.1–2.5 g) * Motor Current (2–10 A) * RPM (900–3000) Publishes telemetry to:
factory/machineX/sensors
Responds to operator commands on:
factory/machineX/cmd
--- ## 📡 **2. Network / Communication Layer — MQTT** MQTT selected because: * Extremely lightweight * Ideal for sensor networks * Supports **bi-directional** communication * Industry standard protocol Message format example:
json
{
  "timestamp": 1764605530.1184,
  "temperature": 67.51,
  "vibration": 0.11,
  "motor_current": 9.51,
  "rpm": 1284
}
--- ## 🖥 **3. Edge / Gateway Layer — Raspberry Pi** File: **edge.py** Pi Responsibilities: ### ✔ Local storage in SQLite ### ✔ Real-time alert detection Thresholds used: * Temperature > **85°C** * Vibration > **2.0 g** * Motor Current > **9 A** ### ✔ Cleansing + forwarding Pi forwards every cleaned packet to **Laptop MQTT Broker**. ### ✔ Inserts into MongoDB Pi updates the cloud DB directly. This mirrors actual factory setups where the edge filters & averages raw machine data. --- ## ☁️ **4. Cloud Platform Layer — Laptop** Includes: ### ✔ MQTT Broker (Mosquitto) Laptop acts as **cloud MQTT broker** for: * receiving edge telemetry * receiving alert messages * handling operator commands ### ✔ MongoDB Cloud Database Collections: * sensor_data * alerts Stores: * machine * timestamp * temperature * vibration * motor_current * rpm --- ## 🖥 **5. Application Layer — Streamlit Neon Dashboard** File: **dashboard_app.py** Pages: ### 🏠 Home Dashboard Machine cards, alerts, status, START/STOP buttons. ### 📈 Analytics Trends for temperature, vibration, current, rpm. ### 📄 Reports Tables + CSV export for sensors and alerts. ### 🛠 Diagnostics * Motor Current Heatmap * RPM Histogram * Vibration FFT * Status Timeline * Predictive failure estimator ### 🧪 System Health * MQTT broker status * MongoDB connection * Pi connectivity * Sensor lag * Packet loss * Network latency --- ## ▶️ **How to Run** ### 1️⃣ Start the MQTT broker (Laptop)
mosquitto -c "C:\Program Files\mosquitto\mosquitto.conf"
### 2️⃣ Run Machine Simulator (Laptop)
python sim_machines_cmd.py
### 3️⃣ Run Edge Node (Raspberry Pi)
python3 edge.py
### 4️⃣ Start HMI Dashboard (Laptop)
streamlit run dashboard_app.py
Dashboard available at:
http://localhost:8501
--- ## 📊 **Demo Flow** 1. Machines generate sensor data → MQTT 2. Edge node processes & forwards data 3. MongoDB stores all telemetry + alerts 4. Dashboard displays real-time metrics 5. User clicks START/STOP → MQTT → Simulator reacts --- ## 🏆 **Results** * Achieved stable multi-layer IIoT pipeline * Real-time neon dashboard for industrial monitoring * Bi-directional MQTT control * Alerts & analytics fully functional * Cloud + edge separation just like real factories --- ## ⚠️ **Challenges Faced** * MQTT port conflicts on Windows * Mosquitto local-only mode behavior * Switching from MongoDB Atlas → local MongoDB * Timestamps inconsistency between simulator & edge * Dashboard refresh latency under data bursts * Designing multi-broker architecture (Pi → Laptop) --- ## 🔮 **Future Improvements** * ML-based predictive maintenance * Add real hardware sensors * Use AWS IoT/GCP IoT Core * OPC-UA integration * CI/CD & containerization (Docker) --- ## 👨‍🎓 **Authors** **Group 4 — MFG 598 Industrial Internet of Things Arizona State University** ---
