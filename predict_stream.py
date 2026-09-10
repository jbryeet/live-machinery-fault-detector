import json
import joblib
import pandas as pd
import websocket
from alerts import send_critical_email

print("🔌 Connecting to live Node.js WebSocket stream...")

ai_brain = joblib.load('trained_machinery_model.pkl')

def on_message(ws, message):
    packet = json.loads(message)
    packet_id = packet['id']
    temp = packet['temperature']
    vib = packet['vibration']
    speed = packet['rotational_speed']
    
    if vib is None:
        vib = 45.0
    features = pd.DataFrame([[temp, vib, speed]], columns=['temperature', 'vibration', 'rotational_speed'])
    
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

ws_url = "ws://localhost:8080"
ws = websocket.WebSocketApp(ws_url,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever()
