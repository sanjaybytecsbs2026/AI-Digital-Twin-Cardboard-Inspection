
import csv
import json
import streamlit as st
import plotly.graph_objects as go

from pathlib import Path

# Project file locations
PROJECT = Path(__file__).resolve().parent.parent

STATE_FILE = PROJECT / "digital_twin" / "twin_state.json"
DATA_FILE = PROJECT / "data" / "sample_sensor_data.csv"

# Dashboard configuration
st.set_page_config(
    page_title="AI-Based Digital Twin",
    page_icon=None,
    layout="wide"
)

# Load Digital Twin state
if not STATE_FILE.exists():
    st.error("Digital Twin state not found. Run digital_twin.py first.")
    st.stop()

with open(STATE_FILE, "r") as file:
    twin = json.load(file)

# Load sensor history
with open(DATA_FILE, "r", newline="") as file:
    history = list(csv.DictReader(file))

# Extract latest sensor values
physical = twin["physical_system"]
acceleration = physical["accelerometer"]
ai_status = twin["ai_analysis"]["status"]

# Dashboard heading - Text only
st.title("AI-Based Digital Twin")
st.caption("Camera-Free | Non-Destructive | AI-Powered Digital Twin")

st.divider()

# Inspection information
st.subheader("Inspection Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Sample ID", twin["sample_id"])
col2.metric("Sound Level", round(physical["sound_level"], 2))
col3.metric("Piezo Response", round(physical["piezo_response"], 3))

st.subheader("AI Inspection Result")

if ai_status == "Normal response":
    st.success("Normal sensor response detected")
else:
    st.warning("Unusual sensor response detected")

st.caption(
    "AI anomaly result based on the saved sensor sample. "
    "It does not prove whether box contents are missing."
)

st.divider()

# Accelerometer readings
st.subheader("Accelerometer Monitoring")

x, y, z = st.columns(3)

x.metric("Acceleration X", round(acceleration["x"], 3))
y.metric("Acceleration Y", round(acceleration["y"], 3))
z.metric("Acceleration Z", round(acceleration["z"], 3))

# Read historical sensor values
sample_ids = [int(row["sample_id"]) for row in history]

acc_x = [float(row["acceleration_x"]) for row in history]
acc_y = [float(row["acceleration_y"]) for row in history]
acc_z = [float(row["acceleration_z"]) for row in history]

# Acceleration graph
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=sample_ids,
    y=acc_x,
    name="X Axis"
))

fig.add_trace(go.Scatter(
    x=sample_ids,
    y=acc_y,
    name="Y Axis"
))

fig.add_trace(go.Scatter(
    x=sample_ids,
    y=acc_z,
    name="Z Axis"
))

fig.update_layout(
    title="Acceleration Sensor History",
    xaxis_title="Sample ID",
    yaxis_title="Acceleration",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# Sound and piezo graphs
st.subheader("Sound and Piezo Monitoring")

sound = [float(row["sound_level"]) for row in history]
piezo = [float(row["piezo_response"]) for row in history]

col1, col2 = st.columns(2)

with col1:
    sound_fig = go.Figure()
    sound_fig.add_trace(go.Scatter(
        x=sample_ids,
        y=sound,
        name="Sound Level"
    ))
    sound_fig.update_layout(
        title="Sound Level History",
        xaxis_title="Sample ID",
        template="plotly_dark"
    )
    st.plotly_chart(sound_fig, use_container_width=True)

with col2:
    piezo_fig = go.Figure()
    piezo_fig.add_trace(go.Scatter(
        x=sample_ids,
        y=piezo,
        name="Piezo Response"
    ))
    piezo_fig.update_layout(
        title="Piezo Response History",
        xaxis_title="Sample ID",
        template="plotly_dark"
    )
    st.plotly_chart(piezo_fig, use_container_width=True)

# Digital Twin information
st.divider()

st.subheader("Digital Twin System Information")

st.write("**System:**", twin["system_name"])
st.write("**Last Updated:**", twin["last_updated"])
st.write("**AI Prediction:**", ai_status)

st.caption(
    "Currently displaying simulated sensor data. "
    "ESP32 hardware integration will be added later."
)

st.success("Digital Twin dashboard loaded successfully!")

