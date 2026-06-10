import time
import joblib
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from alerts import send_critical_email

print("🐕 Live AI Watchdog v2 initialized. Computing probability matrices...")

# 1. Load saved human-coded AI brain
ai_brain = joblib.load('trained_machinery_model.pkl')

# 2. Connect to local PostgreSQL database
db_connection_string = "postgresql://postgres:iapetus@localhost:5432/predictive_maintenance"
db_engine = create_engine(db_connection_string)

last_checked_id = 0

while True:
    try:
        # Fetch the absolute latest telemetry row recorded by the Node.js server
        query = "SELECT id, temperature, vibration, rotational_speed, timestamp FROM telemetry ORDER BY id DESC LIMIT 1;"
        latest_row = pd.read_sql(query, db_engine)
        
        if not latest_row.empty:
            current_id = latest_row['id'].iloc[0]
            
            # Only run the AI if this is a brand new row we haven't seen yet
            if current_id != last_checked_id:
                last_checked_id = current_id
                
                # Extract the sensor features
                temp = latest_row['temperature'].iloc[0]
                vib = latest_row['vibration'].iloc[0]
                speed = latest_row['rotational_speed'].iloc[0]
                db_time = latest_row['timestamp'].iloc[0]
                
                # Human Data Cleaning: Handle the occasional None/Null value
                if pd.isna(vib):
                    vib = 45.0  # Safe fallback baseline for missing values
                
                # Create a mini spreadsheet line for the AI to read
                current_features = pd.DataFrame([[temp, vib, speed]], columns=['temperature', 'vibration', 'rotational_speed'])
                
                # 3. Calculate exact probabilities instead of absolute 0 or 1
                # predict_proba returns [chance_of_0, chance_of_1]. We grab chance_of_1 (failure).
                failure_probability = ai_brain.predict_proba(current_features)[0][1]
                failure_percentage = failure_probability * 100
                
                # Print the upgraded live diagnostic dashboard
                print(f"\n[ID: {current_id}] Temp: {temp}°C | Vib: {vib}Hz | Speed: {speed} RPM")
                print(f"📊 AI Breakdown Risk Calculation: {failure_percentage:.1f}%")
                
                # 4. Action Layer: Define dynamic alert thresholds
                if failure_percentage >= 75.0:
                    print("🚨 ALERT: CRITICAL FAILURE RISK EXCEEDED! PREVENTATIVE ACTION REQUIRED!")
                    send_critical_email("MAC-001", failure_percentage, temp, vib, speed)
                    # Log the incident to a physical text file automatically
                    with open("critical_incidents.log", "a", encoding="utf-8") as log_file:
                        log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ID: {current_id} | "
                                       f"Risk: {failure_percentage:.1f}% | Temp: {temp}°C, Vib: {vib}Hz, Speed: {speed} RPM\n")
                        
                elif failure_percentage >= 35.0:
                    print("⚠️ WARNING: Elevated operational metrics. Monitoring trends closely.")
                else:
                    print("🟢 System Status: Nominal (Healthy)")
                    
    except Exception as err:
        print(f"❌ Error scanning database: {err}")
        
    # Check the database again in 1 second
    time.sleep(1)

