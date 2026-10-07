import streamlit as st
import psutil
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import time

st.set_page_config(page_title="AI Device Health Monitor", page_icon="🛡️", layout="wide")

st.title("🛡️ AI Device Health Monitoring System")
st.markdown("Welcome to our AI & ML club exhibition project! This dashboard monitors real-time system metrics and uses a **Linear Regression ML model** to forecast future resource spikes.")

# Placeholder for live metrics
placeholder = st.empty()

# Store historical data in session state to train our regression model
if 'history' not in st.session_state:
    st.session_state.history = []

# Simulation loop for live monitoring
for i in range(1, 11):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    st.session_state.history.append({'second': i, 'cpu_usage': cpu, 'ram_usage': ram})
    
    df = pd.DataFrame(st.session_state.history)
    
    with placeholder.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("CPU Usage", f"{cpu}%")
        col2.metric("RAM Usage", f"{ram}%")
        col3.metric("Disk Usage", f"{disk}%")
        
        st.subheader("📊 System Log & Trend Analysis")
        
        # 👉 ADD THE LINE CHART RIGHT HERE 👈
        st.line_chart(df[['cpu_usage', 'ram_usage']])
        
        # Display the data table below the chart
        st.dataframe(df)
        
        # Apply Linear Regression if we have at least 3 data points
        if len(df) >= 3:
            X = df[['second']] # Independent variable (time)
            y = df['cpu_usage'] # Dependent variable (CPU usage)
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict CPU usage for 5 seconds into the future
            future_seconds = np.array([[len(df) + 1], [len(df) + 2], [len(df) + 3], [len(df) + 4], [len(df) + 5]])
            predictions = model.predict(future_seconds)
            
            st.info(f"🤖 **AI Linear Regression Forecast:** Projected CPU usage in 5 seconds is approximately **{predictions[-1]:.1f}%**.")

st.success("Scan Complete! Exhibition Report Generated with Predictive ML.")