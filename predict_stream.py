import json
import joblib
import pandas as pd
import websocket
from alerts import send_critical_email

print("🔌 Connecting to live Node.js WebSocket stream...")

# Load our saved human-coded AI brain
ai_brain = joblib.load('trained_machinery_model.pkl')

def on_message(ws, message):
    # This function triggers the exact millisecond a packet is broadcasted by Node!
    packet = json.loads(message)
    
    # Extract metrics
    packet_id = packet['id']
    temp = packet['temperature']
    vib = packet['vibration']
    speed = packet['rotational_speed']
    
    # Human Data Cleaning: Handle the occasional None/Null value
    if vib is None:
        vib = 45.0
        
    # Format data for Scikit-Learn
    features = pd.DataFrame([[temp, vib, speed]], columns=['temperature', 'vibration', 'rotational_speed'])
    
    # Run the prediction matrix
    failure_probability = ai_brain.predict_proba(features)[0][1]
    failure_percentage = failure_probability * 100
    
    print(f"\n⚡ [STREAMED READ] ID: {packet_id} | Temp: {temp}°C | Vib: {vib}Hz | Speed: {speed} RPM")
    print(f"📊 Live AI Risk Evaluation: {failure_percentage:.1f}%")
    
    if failure_percentage >= 75.0:
        print("🚨 ALERT: CRITICAL MACHINE RISK SEEN ON THE WIRE!")
        send_critical_email("MAC-001", failure_percentage, temp, vib, speed)
    elif failure_percentage >= 35.0:
        print("⚠️ WARNING: Elevated metrics detected in stream.")
    else:
        print("🟢 System Status: Nominal (Healthy)")

def on_error(ws, error):
    print(f"❌ Stream Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 Stream disconnected.")

# Open connection link directly to the Node socket backend
ws_url = "ws://localhost:8080"
ws = websocket.WebSocketApp(ws_url,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever()