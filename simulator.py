import time
import random
import requests

# Target URL pointing to our local Node.js backend
server_url = "http://localhost:3000/api/telemetry"
machine_name = "MAC-001"

print("🚀 Starting manual machine simulator loop...")

while True:
    # 1. Decide randomly if the machine is working normally or acting up
    # Let's say it has a 10% chance of acting up
    is_failing = random.randint(1, 10) == 1
    
    if is_failing:
        # High temperature and high vibration spikes
        temperature = round(random.uniform(92.0, 108.0), 2)
        vibration = round(random.uniform(62.0, 85.0), 2)
        rotational_speed = round(random.uniform(2200.0, 2800.0), 1)
    else:
        # Safe running parameters
        temperature = round(random.uniform(70.0, 85.0), 2)
        vibration = round(random.uniform(25.0, 42.0), 2)
        rotational_speed = round(random.uniform(1500.0, 1800.0), 1)

    # 2. Every now and then, let's simulate a loose sensor wire (missing data)
    # We will randomly set vibration to None (null) 5% of the time
    if random.randint(1, 20) == 1:
        vibration = None
        print("⚠️ Sensor Warning: Vibration signal dropped momentarily.")

    # 3. Create a standard dictionary to hold our data
    data_packet = {
        "machine_id": machine_name,
        "temperature": temperature,
        "vibration": vibration,
        "rotational_speed": rotational_speed
    }
    
    # 4. Try sending it over the network to our Express backend
    try:
        response = requests.post(server_url, json=data_packet)
        print(f"Data Sent -> Status: {response.status_code} | Temp: {temperature} | Vib: {vibration}")
    except Exception as err:
        print(f"❌ Failed to reach the server: {err}")
        
    # Wait 1 second before reading the sensors again
    time.sleep(1)