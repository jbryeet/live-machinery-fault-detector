import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

print("📊 Initializing Automated Production Report Generator...")

# 1. Connect to our local PostgreSQL database
db_connection_string = "postgresql://postgres:iapetus@localhost:5432/predictive_maintenance"
db_engine = create_engine(db_connection_string)

# 2. Extract database telemetry data
try:
    sql_query = "SELECT id, temperature, vibration, rotational_speed, timestamp FROM telemetry ORDER BY id ASC;"
    df = pd.read_sql(sql_query, db_engine)
except Exception as e:
    print(f"❌ Failed to extract reporting matrix: {e}")
    exit()

if df.empty:
    print("⚠️ No logged metrics available inside the database to formulate a report.")
    exit()

total_records = len(df)

# 3. Process human-level data insights
# Identify failures using our established operational logic
failure_conditions = (df['temperature'] > 90.0) & (df['vibration'] > 60.0)
df['is_failure'] = failure_conditions.astype(int)

total_failures = df['is_failure'].sum()
total_healthy = total_records - total_failures
failure_percentage = (total_failures / total_records) * 100

# Extract the maximum metrics recorded
max_temp = df['temperature'].max()
max_vib = df['vibration'].max()

# Grab the specific lines where anomalies were highest
highest_risk_events = df[failure_conditions].sort_values(by='temperature', ascending=False).head(5)

# 4. Generate the Markdown Report file
current_date = datetime.now().strftime("%B %d, %Y - %H:%M")
report_filename = "machinery_health_report.md"

with open(report_filename, "w", encoding="utf-8") as file:
    file.write(f"# 📈 Industrial Machinery Health & Analytics Report\n\n")
    file.write(f"**Generated On:** {current_date}  \n")
    file.write(f"**Target System Endpoint:** `MAC-001`  \n\n")
    file.write(f"---\n\n")
    
    file.write(f"## 📊 Executive Summary Metrics\n")
    file.write(f"* **Total Telemetry Packets Evaluated:** {total_records}\n")
    file.write(f"* **Nominal Operational Readings (Healthy):** {total_healthy}\n")
    file.write(f"* **Critical AI Anomaly Triggers (High Risk):** {total_failures}\n")
    file.write(f"* **Systemic Failure Ratio:** {failure_percentage:.2f}%\n\n")
    
    file.write(f"## 🌡️ Absolute Hardware Limits Reached\n")
    file.write(f"* **Peak Core Temperature:** {max_temp}°C\n")
    file.write(f"* **Maximum Peak Oscillation / Vibration:** {max_vib} Hz\n\n")
    
    file.write(f"## 🚨 Top 5 Most Severe Systemic Anomaly Events\n")
    file.write(f"Below are the highest temperature alerts extracted from historical records:\n\n")
    file.write(f"| Event ID | Temperature | Vibration | Rotational Speed | System Timestamp |\n")
    file.write(f"| --- | --- | --- | --- | --- |\n")
    
    for idx, row in highest_risk_events.iterrows():
        file.write(f"| {row['id']} | {row['temperature']}°C | {row['vibration']} Hz | {row['rotational_speed']} RPM | {row['timestamp']} |\n")

print(f"✅ Success! Analysis completed. Report compiled into: '{report_filename}'")