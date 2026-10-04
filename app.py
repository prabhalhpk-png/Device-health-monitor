import streamlit as st
import psutil
import pandas as pd
import time

# --- WEB PAGE CONFIG ---
st.set_page_config(page_title="AI Device Health Monitor", page_icon="🛡️", layout="centered")

st.title("🛡️ AI Device Health Monitoring System")
st.write("Welcome to our AI & ML club exhibition project! This dashboard monitors real-time system metrics and uses a custom AI anomaly detector to flag hardware spikes.")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Control Panel")
scan_duration = st.sidebar.slider("Scan Duration (seconds)", min_value=5, max_value=30, value=10)
start_button = st.sidebar.button("🚀 Start Live Health Scan")

# --- MAIN APP LOGIC ---
if start_button:
    st.subheader("📡 Live Monitoring in Progress...")
    
    # Placeholders for live updates on the web page
    metric_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    health_logs = []
    
    for i in range(scan_duration):
        # Grab live system metrics
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        health_logs.append({
            "second": i + 1,
            "cpu_usage": cpu,
            "ram_usage": ram,
            "disk_usage": disk
        })
        
        # Update live metrics on the web page
        with metric_placeholder.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("CPU Usage", f"{cpu}%")
            col2.metric("RAM Usage", f"{ram}%")
            col3.metric("Disk Usage", f"{disk}%")
            
        # Update progress bar
        progress_bar.progress((i + 1) / scan_duration)

    # --- AI & STATISTICAL ANOMALY DETECTION ---
    df = pd.DataFrame(health_logs)
    avg_cpu = df['cpu_usage'].mean()

    def check_anomaly(row):
        if row['cpu_usage'] > 85 or row['cpu_usage'] > (avg_cpu + 15):
            return "⚠️ Spike / Anomaly Detected!"
        else:
            return "Normal"

    df['status'] = df.apply(check_anomaly, axis=1)

    # --- EXHIBITION REPORT & DASHBOARD DISPLAY ---
    st.success("✅ Scan Complete! Exhibition Report Generated:")
    
    # Show key stats summary cards
    col_a, col_b = st.columns(2)
    col_a.metric("Session Average CPU", f"{avg_cpu:.1f}%")
    col_b.metric("Total Data Points", len(df))
    
    # Show data table
    st.write("### 📊 System Log Table")
    st.dataframe(df)
    
    # Show interactive trend chart
    st.write("### 📈 Performance Trend Chart")
    st.line_chart(df.set_index('second')[['cpu_usage', 'ram_usage']])