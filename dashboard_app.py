# ---------------------------------------------------------------
#  IIOT MULTI-PAGE NEON DASHBOARD (FINAL VERSION - FIXED BUTTONS)
# ---------------------------------------------------------------
#   ✓ Neon Green START
#   ✓ Neon Red STOP
#   ✓ CSS now Works 100%
#   ✓ HTML buttons instead of st.button()
# ---------------------------------------------------------------

import json
import time
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
import paho.mqtt.publish as publish

# ================================================================
# CONFIG
# ================================================================
LAPTOP_MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "iiot_cloud"

PI_MQTT_HOST = "10.117.162.70"  # Raspberry Pi IP
PI_MQTT_PORT = 1883

LAPTOP_MQTT_HOST="10.117.162.51"
LAPTOP_MQTT_PORT =1883

MACHINES = ["machine1", "machine2", "machine3","machine4"]


# ================================================================
# DB FUNCTIONS
# ================================================================
@st.cache_resource
def get_mongo():
    client = MongoClient(LAPTOP_MONGO_URI)
    return client[DB_NAME]


def load_sensor_data(limit=500):
    coll = get_mongo()["sensor_data"]
    docs = list(coll.find().sort("timestamp", -1).limit(limit))
    if not docs:
        return pd.DataFrame()
    df = pd.DataFrame(docs)
    df["time"] = pd.to_datetime(df["timestamp"], unit="s")
    return df.sort_values("time")


def load_alerts(limit=30):
    coll = get_mongo()["alerts"]
    docs = list(coll.find().sort("timestamp", -1).limit(limit))
    for d in docs:
        d["time"] = datetime.fromtimestamp(d["timestamp"])
    return docs


# ================================================================
# MQTT COMMANDS
# ================================================================
def send_command(machine, cmd):
    topic = f"factory/{machine}/cmd"
    payload = json.dumps({"command": cmd})
    try:
        publish.single(topic, payload, hostname=PI_MQTT_HOST, port=PI_MQTT_PORT)
        st.toast(f"Sent {cmd.upper()} to {machine}", icon="🎮")
    except Exception as e:
        st.error(f"Error sending command: {e}")


# ================================================================
# CATCH HTML BUTTON COMMANDS (IMPORTANT)
# ================================================================
params = st.query_params
if "cmd" in params and "machine" in params:
    send_command(params["machine"], params["cmd"])


# ================================================================
# GLOBAL THEME CSS
# ================================================================
st.set_page_config(page_title="IIoT Neon Dashboard", layout="wide")

st.markdown(
    """
<style>

body { background-color: #050b1a; }

.stApp {
    background: radial-gradient(circle at top, #111b3a 0, #050b1a 45%, #020612 100%);
    color: #f5f7ff;
    font-family: "Segoe UI", sans-serif;
}

/* Generic cards */
.card {
    background: linear-gradient(145deg, #061022, #0c1530);
    border-radius: 20px;
    padding: 16px;
    border: 1px solid rgba(0,255,255,0.25);
    box-shadow: 0 0 18px rgba(0,255,255,0.18);
}

/* Alerts list */
.alert-card {
    background: linear-gradient(145deg, #2c1016, #3a1015);
    padding: 12px;
    border-radius: 12px;
    border-left: 4px solid #ff4b4b;
    margin-bottom: 8px;
}

/* Machine status cards */
.machine-card {
    padding: 18px;
    border-radius: 18px;
    background: linear-gradient(140deg, #071223, #101c35);
    border: 1px solid rgba(0,255,200,0.3);
    box-shadow: 0 0 14px rgba(0,255,255,0.18);
}

/* Running / Stopped text */
.status-ok {
    color: #00ff9d;
    font-weight: bold;
}
.status-stop {
    color: #ff5e5e;
    font-weight: bold;
}

/* ====================== */
/*   CUSTOM HTML BUTTONS   */
/* ====================== */

/* START BUTTON (GREEN NEON) */
.start-btn {
    background: linear-gradient(145deg, #00ff80, #00cc66);
    color: white;
    padding: 10px 26px;
    border-radius: 12px;
    border: none;
    font-size: 16px;
    font-weight: 900;
    width: 100%;
    cursor: pointer;
    box-shadow: 0 0 14px #00ff80, 0 0 30px #00cc66;
}
.start-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 0 18px #00ff99, 0 0 40px #00e67a;
}

/* STOP BUTTON (RED NEON) */
.stop-btn {
    background: linear-gradient(145deg, #ff4060, #d92040);
    color: white;
    padding: 10px 26px;
    border-radius: 12px;
    border: none;
    font-size: 16px;
    font-weight: 900;
    width: 100%;
    cursor: pointer;
    box-shadow: 0 0 14px #ff4d6d, 0 0 30px #ff0033;
}
.stop-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #ff4d6d, 0 0 40px #ff0033;
}

</style>
""",
    unsafe_allow_html=True,
)


# Helper to style plotly figs
def style_fig(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,10,25,0.9)",
        font_color="#f5f7ff",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


# ================================================================
# SIDEBAR NAVIGATION
# ================================================================

# Inject custom CSS
st.markdown("""
<style>

/* ---- Sidebar background ---- */
section[data-testid="stSidebar"] {
    background-color: #0a0f24;   /* Dark blue / gaming style */
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Sidebar title "📌 Navigation" */
.sidebar .sidebar-content h2, 
section[data-testid="stSidebar"] h2 {
    color: #39FF14 !important;    /* Neon green */
    font-size: 22px !important;
    font-weight: 700 !important;
}

/* Radio option labels */
div[role="radiogroup"] > label {
    color: #00BFFF !important;    /* Neon blue */
    font-size: 20px !important;   /* Increase size */
    font-weight: 600 !important;
    padding: 6px 4px;
}

</style>
""", unsafe_allow_html=True)


page = st.sidebar.radio("📌 Navigation", ["Home", "Analytics", "Reports","Diagnostics","System Health"])


st.markdown("""
<style>

.overview-box {
    background: #0c1a2a;
    border: 1px solid #1e3a5f;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 18px;
}

.overview-title {
    color: #00BFFF;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 6px;
}

.overview-value {
    color: #e0f3ff;
    font-size: 24px;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

# ================================================================
# PAGE 1 — HOME DASHBOARD
# ================================================================
if page == "Home":
    st.markdown("<h1 style='color:#e0f3ff;'>🏭 IIoT Factory Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("")
    
    df = load_sensor_data()
    alerts = load_alerts()

    # ================================================================
# OVERVIEW ROW — directly under the dashboard title
# ================================================================
    st.markdown("<div class='card'><h3>📊 Overview</h3>", unsafe_allow_html=True)

    o1, o2, o3 = st.columns(3)   # 3 equal columns

        
    with o1:
        st.markdown(
            f"""
            <div class='overview-box'>
                <div class='overview-title'>📘 Records</div>
                <div class='overview-value'>{len(df)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with o2:
        st.markdown(
            f"""
            <div class='overview-box'>
                <div class='overview-title'>🔥 Avg Temp</div>
                <div class='overview-value'>{df['temperature'].mean():.1f} °C</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with o3:
        st.markdown(
            f"""
            <div class='overview-box'>
                <div class='overview-title'>🚨 Active Alerts</div>
                <div class='overview-value'>{len(alerts)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
    colA, colB = st.columns([1, 2.2])

    # ------------------ ALERTS ------------------
    with colA:
        st.markdown("<div class='card'><h3>🚨 Alerts</h3> <h5>Limts</h5><b>Temp:85°C &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Vibration:2.0G  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  Motor_current:9   </b></div>", unsafe_allow_html=True)


        st.markdown("<div> </div>",unsafe_allow_html=True)
        if not alerts:
            st.write("No recent alerts.")
        else:
            for a in alerts[:6]:
                st.markdown(
                    f"""
                    <div class='alert-card'>
                        <b>{a['alert_type']}</b><br>
                        {a['machine']} • Value: {a['value']}<br>
                        <span style='opacity:0.7;font-size:12px'>{a['time']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------ MACHINE CARDS ------------------
    with colB:
        st.markdown("<div class='card'><h3 >🖥 Machine Status</h3>", unsafe_allow_html=True)
        
        st.markdown("<div></div>",unsafe_allow_html=True)

        if df.empty:
            st.warning("No data yet.")
        else:
            latest = df.groupby("machine").tail(1)
            cols = st.columns(4)

            for i, machine in enumerate(MACHINES):
                with cols[i]:

                    if machine not in latest["machine"].values:
                        st.markdown(
                            f"<div class='machine-card'>No data for {machine}</div>",
                            unsafe_allow_html=True,
                        )
                        continue

                    row = latest[latest["machine"] == machine].iloc[0]
                    running = time.time() - row["timestamp"] < 5

                    status_class = "status-ok" if running else "status-stop"
                    status_text = "RUNNING" if running else "STOPPED"

                    # Machine card
                    st.markdown(
                        f"""
                        <div class='machine-card'>
                        <h4>{machine.upper()}</h4>
                        <div class='{status_class}'>{status_text}</div><br>
                        <b>🌡️Temp:</b> {row['temperature']:.2f} °C<br>
                        <br>
                        <b>📳Vibration:</b> {row['vibration']:.2f} G<br>
                        <br>
                        <b>⚡Current:</b> {row['motor_current']:.2f} A<br>
                        <br>
                        <b>⚙️RPM:</b> {row['rpm']}<br><br>
                        <br>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown("<div></div>",unsafe_allow_html=True)
                    # ----------------------
                    # Neon Start/Stop Buttons (HTML)
                    # ----------------------
                    st.markdown(
                        f"""
                        <form action="" method="get">
                            <input type="hidden" name="cmd" value="start">
                            <input type="hidden" name="machine" value="{machine}">
                            <button class="start-btn">START</button>
                        </form>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown("<div></div>",unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <form action="" method="get">
                            <input type="hidden" name="cmd" value="stop">
                            <input type="hidden" name="machine" value="{machine}">
                            <button class="stop-btn">STOP</button>
                        </form>
                        """,
                        unsafe_allow_html=True,
                    )

        st.markdown("</div>", unsafe_allow_html=True)

    

             


# ================================================================
# PAGE 2 — ANALYTICS
# ================================================================
elif page == "Analytics":
    st.markdown("<h1 style='color:#e0f3ff;'>📈 Machine Analytics</h1>", unsafe_allow_html=True)
    df = load_sensor_data()
    if df.empty:
        st.warning("No data available.")
    else:
        machine = st.selectbox("Select Machine", MACHINES)
        mdf = df[df["machine"] == machine]

        st.subheader("Temperature Trend")
        fig1 = px.line(mdf, x="time", y="temperature")
        style_fig(fig1)
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Vibration Trend")
        fig2 = px.line(mdf, x="time", y="vibration")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Current Trend")
        fig3 = px.line(mdf, x="time", y="motor_current")
        style_fig(fig3)
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("RPM Trend")
        fig4 = px.line(mdf, x="time", y="rpm")
        style_fig(fig4)
        st.plotly_chart(fig4, use_container_width=True)


# ================================================================
# PAGE 3 — REPORTS (Sensors + Alerts)
# ================================================================
elif page == "Reports":

    st.markdown("<h1 style='color:#e0f3ff;'>📄 Reports</h1>", unsafe_allow_html=True)

    df = load_sensor_data()
    alerts = load_alerts()

    if df.empty:
        st.warning("No data to display.")
    else:
        # ---------------------- MACHINE FILTER ----------------------
        machine = st.selectbox("Filter by Machine", ["All"] + MACHINES)

        # Apply filter on sensor data
        df_filtered = df.copy()
        if machine != "All":
            df_filtered = df_filtered[df_filtered["machine"] == machine]

        # Apply filter on alerts
        alerts_filtered = []
        if machine == "All":
            alerts_filtered = alerts
        else:
            alerts_filtered = [a for a in alerts if a["machine"] == machine]

        # ---------------------- SENSOR DATA TABLE ----------------------
        st.markdown("### 📊 Sensor Data (Latest 200 rows)", unsafe_allow_html=True)

        st.dataframe(df_filtered.tail(200), use_container_width=True)

        # Download Sensor CSV
        sensor_csv = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Sensor Data CSV",
            sensor_csv,
            "sensor_data.csv",
            "text/csv",
        )

        st.write("---")

        # ---------------------- ALERTS DATA TABLE ----------------------
        st.markdown("### 🚨 Alerts Data", unsafe_allow_html=True)

        if alerts_filtered:
            alert_df = pd.DataFrame(alerts_filtered)
            alert_df["time"] = alert_df["time"].astype(str)
            st.dataframe(alert_df, use_container_width=True)

            # Download Alerts CSV
            alert_csv = alert_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Alerts CSV",
                alert_csv,
                "alerts_data.csv",
                "text/csv",
            )
        else:
            st.info("No alerts for the selected machine.")

# ================================================================
# PAGE — DIAGNOSTICS (Maintenance View)
# ================================================================
elif page == "Diagnostics":
    st.markdown("<h1 style='color:#7de8ff;'>🛠 Diagnostics & Machine Health</h1>", unsafe_allow_html=True)

    df = load_sensor_data()

    if df.empty:
        st.warning("No sensor data available yet.")
        st.stop()

    # Choose machine
    machine = st.selectbox("Select Machine", MACHINES)

    mdf = df[df["machine"] == machine].tail(300)

    st.write("")

    # ---------------------------
    # CARD ROW 1 — HEATMAP + HISTOGRAM
    # ---------------------------
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='card'><h3 style='color:#80ffd6;'>⚡ Motor Current Heatmap</h3>", unsafe_allow_html=True)

        fig_heat = px.density_heatmap(
            mdf,
            x="time",
            y="motor_current",
            nbinsx=20,
            nbinsy=20,
            color_continuous_scale="turbo",
            title=""
        )
        fig_heat.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(3,8,18,0.9)"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'><h3 style='color:#ffcc7a;'>🌀 RPM Histogram</h3>", unsafe_allow_html=True)

        fig_hist = px.histogram(
            mdf,
            x="rpm",
            nbins=20,
            color_discrete_sequence=["#ffaa44"]
        )
        fig_hist.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(18,10,3,0.9)"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ---------------------------
    # CARD ROW 2 — FFT + STATUS TIMELINE
    # ---------------------------
    d1, d2 = st.columns(2)

    # ----- Synthetic FFT for vibration -----
    import numpy as np

    vib = mdf["vibration"].values
    vib = vib - vib.mean()
    fft_vals = np.abs(np.fft.rfft(vib))
    fft_freqs = np.fft.rfftfreq(len(vib), d=0.1)

    with d1:
        st.markdown("<div class='card'><h3 style='color:#9dbbff;'>📡 Vibration Frequency Spectrum (FFT)</h3>", unsafe_allow_html=True)

        fig_fft = px.line(
            x=fft_freqs,
            y=fft_vals,
            labels={"x": "Frequency (Hz)", "y": "Amplitude"},
        )
        fig_fft.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(4,6,25,0.9)"
        )
        st.plotly_chart(fig_fft, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ----- Machine Status Timeline -----
    mdf["status"] = ["RUNNING" if (time.time() - ts) < 5 else "STOPPED" for ts in mdf["timestamp"]]

    with d2:
        st.markdown("<div class='card'><h3 style='color:#55ff9d;'>⏱ Status Timeline</h3>", unsafe_allow_html=True)

        fig_timeline = px.scatter(
            mdf,
            x="time",
            y="status",
            color="status",
            color_discrete_map={"RUNNING": "#00ff9d", "STOPPED": "#ff5959"},
            title=""
        )
        fig_timeline.update_traces(marker=dict(size=10))
        fig_timeline.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6,18,10,0.9)"
        )

        st.plotly_chart(fig_timeline, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ---------------------------
    # CARD ROW 3 — ERROR LOGS + PREDICTED FAILURES
    # ---------------------------
    
    st.markdown("<div class='card'><h3 style='color:#f2ff7e;'>🔮 Predicted Failures</h3>", unsafe_allow_html=True)

    temp_avg = mdf["temperature"].mean()
    vib_avg = mdf["vibration"].mean()
    curr_avg = mdf["motor_current"].mean()

    if temp_avg > 80 or vib_avg > 2.2 or curr_avg > 8:
        st.error("⚠️ High chance of failure within next 2 hours.")
    elif temp_avg > 60:
        st.warning("⚠️ Moderate overheating risk detected.")
    else:
        st.success("🟢 No predicted failures. Machine stable.")

    st.markdown("</div>", unsafe_allow_html=True)


# ================================================================
# PAGE — SYSTEM HEALTH
# ================================================================
elif page == "System Health":
    st.markdown("<h1 style='color:#77d7ff;'>🩺 System Health Monitor</h1>", unsafe_allow_html=True)

    df = load_sensor_data()
    alerts = load_alerts()

    # ------------------------------------------------------------
    # Helper – Test MongoDB Connection
    # ------------------------------------------------------------
    def check_mongo():
        try:
            client = MongoClient(LAPTOP_MONGO_URI, serverSelectionTimeoutMS=2000)
            client.server_info()
            return True
        except:
            return False

    # ------------------------------------------------------------
    # Helper – Test MQTT
    # ------------------------------------------------------------
    def check_mqtt():
        try:
            publish.single("factory/health/test", "ok",
                           hostname=LAPTOP_MQTT_HOST,
                           port=LAPTOP_MQTT_PORT
                           )
            return True
        except Exception as e:
            print("MQTT CHECK FAILED:",e)
            return False

    # ------------------------------------------------------------
    # Helper – Pi ping
    # ------------------------------------------------------------
    import os

    def ping_pi():
        try:
            response = os.system(f"ping -n 1 {PI_MQTT_HOST} >nul")
            return response == 0
        except:
            return False

    # ------------------------------------------------------------
    # Helper – Sensor Lag
    # ------------------------------------------------------------
    def get_sensor_lag():
        if df.empty:
            return None
        latest_ts = df["timestamp"].max()
        return round(time.time() - latest_ts, 2)

    # ------------------------------------------------------------
    # Helper – Packet Loss (simple rule)
    # ------------------------------------------------------------
    def packet_loss():
        if df.empty:
            return None
        total = len(df)
        unique_ts = df["timestamp"].nunique()
        loss = 1 - (unique_ts / total)
        return round(loss * 100, 2)

    # ------------------------------------------------------------
    # CARD LAYOUT
    # ------------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    # ================= MQTT Broker =================
    with c1:
        ok = check_mqtt()
        color = "#00ff9d" if ok else "#ff5b5b"

        st.markdown(f"""
        <div class='card'>
        <h3 style='color:#7de8ff;'>📡 MQTT Broker</h3>
        <h2 style='color:{color};'>
            {"ONLINE" if ok else "OFFLINE"}
        </h2>
        <small>Broker IP: {LAPTOP_MQTT_HOST}:{LAPTOP_MQTT_PORT}</small>
        </div>
        """, unsafe_allow_html=True)

    # ================= MongoDB =================
    with c2:
        ok = check_mongo()
        color = "#00ff9d" if ok else "#ff5b5b"

        st.markdown(f"""
        <div class='card'>
        <h3 style='color:#7de8ff;'>🗄 MongoDB</h3>
        <h2 style='color:{color};'>
            {"CONNECTED" if ok else "NOT CONNECTED"}
        </h2>
        <small>URI: localhost:27017</small>
        </div>
        """, unsafe_allow_html=True)

    # ================= Edge Device (Pi) =================
    with c3:
        ok = ping_pi()
        color = "#00ff9d" if ok else "#ff5b5b"

        st.markdown(f"""
        <div class='card'>
        <h3 style='color:#7de8ff;'>🤖 Edge Device (Raspberry Pi)</h3>
        <h2 style='color:{color};'>
            {"ONLINE" if ok else "OFFLINE"}
        </h2>
        <small>Ping test: {"Success" if ok else "Failure"}</small>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    c4, c5, c6 = st.columns(3)

    # ================= SENSOR LAG =================
    with c4:
        lag = get_sensor_lag()
        if lag is None:
            value = "No Data"
            color = "#ffb95e"
        else:
            color = "#00ff9d" if lag < 5 else "#ffb95e" if lag < 10 else "#ff5b5b"
            value = f"{lag} sec"

        st.markdown(f"""
        <div class='card'>
        <h3 style='color:#9bd8ff;'>⏱ Sensor Stream Lag</h3>
        <h2 style='color:{color};'>{value}</h2>
        <small>Time since last sensor packet</small>
        </div>
        """, unsafe_allow_html=True)

    # ================= PACKET LOSS =================
    with c5:
        loss = packet_loss()
        if loss is None:
            value = "No Data"
            color = "#ffb95e"
        else:
            color = "#00ff9d" if loss < 2 else "#ffb95e" if loss < 5 else "#ff5b5b"
            value = f"{loss}%"

        st.markdown(f"""
        <div class='card'>
        <h3 style='color:#ffcc7a;'>📉 Packet Loss</h3>
        <h2 style='color:{color};'>{value}</h2>
        <small>Based on duplicate timestamps</small>
        </div>
        """, unsafe_allow_html=True)

    # ================= LATENCY =================
    with c6:
        ok = ping_pi()
        value = "Low" if ok else "High"
        color = "#00ff9d" if ok else "#ff5b5b"

        st.markdown(f"""
        <div class='card'>
        <h3 style='color:#c8b8ff;'>🌐 Network Latency</h3>
        <h2 style='color:{color};'>{value}</h2>
        <small>Basic ping check to Raspberry Pi</small>
        </div>
        """, unsafe_allow_html=True)
