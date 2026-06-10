# Real-Time Industrial Machinery Stream and Predictive Maintenance Pipeline

This project is a decoupled, real-time data streaming pipeline and machine learning system built to monitor industrial machinery health and predict equipment failures before they happen. The pipeline transitions from simple HTTP logging to a zero-lag WebSocket stream, feeding live data straight into a trained machine learning model.

How the System Works
Instead of processing an old, static dataset offline, this project runs a live four-stage data architecture:
## The Machine Simulator (simulator.py):
A Python script that acts as an on-site machine endpoint. It continuously streams sensor metrics like temperature, vibration, and rotation speed. To mimic real-world conditions, it includes random transmission drops (missing values) and data overlap where normal operations look similar to early-stage failures.
## The Ingestion Gateway (server.js):
A Node.js and Express backend that provides a REST API for the simulator to talk to. The exact millisecond a data packet hits this gateway, the server logs it to a database and broadcasts the raw payload over a WebSocket channel on port 8080.
## The Relational Storage (PostgreSQL):
A local database that catches and logs every single packet sequentially with a timestamp for long-term historical record-keeping and batch analysis.
## The Live AI Engine (predict_stream.py):
A standalone Python watchdog script that opens a permanent WebSocket link to the server. It grabs incoming sensor data straight out of the stream, fills in missing values manually using a calculated historical average, and runs the data through a saved Scikit-Learn model to output a live breakdown risk percentage (from 0% to 100%).

Code Architecture
server.js - Express API backend and WebSocket broadcast server.
simulator.py - Script simulating active machinery data with realistic sensor noise.
train_model.py - Script that loads historical SQL logs, handles data cleaning, trains a Random Forest model, and saves it to a file.
predict_stream.py - The live stream consumer that catches WebSocket packets and evaluates failure probability in real-time.
predict_live.py - An alternative watchdog version that scans the database using structured polling queries.
generate_report.py - A reporting tool that queries the database to build a markdown analytics summary of past errors.
alerts.py - A dedicated mail handling script that triggers HTML emergency dispatch messages when risk calculations exceed 75%.

# Local Setup and Database Configuration
Run the following script in your PostgreSQL query tool to initialize the core tracking table and its optimization index:

SQL
CREATE TABLE telemetry (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(50),
    temperature NUMERIC(5, 2),
    vibration NUMERIC(5, 2),
    rotational_speed NUMERIC(6, 1),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index created to speed up time-series lookups
CREATE INDEX idx_telemetry_machine_time ON telemetry (machine_id, timestamp DESC);

# Tech Stack & Engineering Justification
This project avoids bloated external frameworks or heavy enterprise automation platforms, relying instead on native, lightweight components to maximize data processing speed and minimize network overhead.
## 1. Telemetry & Simulation Layer
Python 3 (random, time): Used to build the machinery simulator. Python’s native math and timing libraries allow for lightweight, stateful loops that mimic active hardware data streams with low system overhead.
## 2. Ingestion & Core Network Routing
Node.js & Express: Serves as the primary REST API endpoint gateway. Express was chosen because its asynchronous, event-driven, non-blocking I/O model handles high-frequency incoming HTTP requests efficiently without bottlenecking the system.
ws (Native Node WebSocket Library): Used to implement real-time data streaming. Instead of forcing the AI layer to repeatedly query the hard drive for updates, ws sets up an open TCP channel to broadcast incoming sensor data packets instantly.
## 3. Data Persistence Layer
PostgreSQL: A robust relational database server used to log chronological sequences permanently. SQL structure allows for precise, historical time-series queries and manual data inspection.
pg (Node-Postgres Client): Configured with connection pooling to handle frequent database reads and writes simultaneously without exhausting network resources.
## 4. Machine Learning & Predictive Analytics
Pandas & NumPy: Used within the Python scripts to handle data structure manipulation. It provides the clean matrix operations needed to compute historical moving averages and perform manual data imputation (.fillna()).
Scikit-Learn (RandomForestClassifier): Chosen for the core machine learning model. Random Forest structures handle mixed, overlapping sensor distributions cleanly and are highly resistant to overfitting when processing noisy data.
Joblib: Used to serialize (freeze) the trained weights of the machine learning classifier, enabling the live script to instantly load the model into memory without retraining it on launch.
## 5. Automation & Notifications
smtplib & email.mime (Python Standard Library): Used to establish secure TLS handshakes with external mail relays. It structures raw script outputs into formatted HTML alert messages to dispatch emergency updates to technical staff.

# Project Development Timeline and Changelog
June 11, 2026 — Phase 5: Real-Time WebSocket Streaming
Milestone: Upgraded the pipeline from database polling to a live streaming architecture.
Technical Updates:
Added the ws library to server.js to broadcast incoming sensor packets immediately.
Created predict_stream.py to open a permanent network socket, removing the need to repeatedly query the database disk for live predictions.
Added probability confidence scores (predict_proba) to show a dynamic risk percentage instead of a simple safe/broken answer.

June 08, 2026 — Phase 4: Automated Reporting and Alert Triggers
Milestone: Built a forensic analytics engine and a critical notification system.
Technical Updates:
Wrote generate_report.py to pull historical database rows, evaluate machine uptime metrics, and export them into a markdown document.
Created alerts.py using Python's native smtplib to construct and queue HTML emergency alerts when the AI flags a risk score above 75%.

June 04, 2026 — Phase 3: PostgreSQL Integration and Serialization
Milestone: Added database logging and configured model saving.
Technical Updates:
Integrated connection pooling into the Express API using the pg client driver.
Added joblib functionality to the training script to freeze and save the trained Scikit-Learn Random Forest classifier to a local file.

May 30, 2026 — Phase 2: Cross-Language Network Bridge
Milestone: Connected the isolated Python environment to the Node.js backend.
Technical Updates:
Implemented the Python requests library to stream simulation data over HTTP POST requests.
Formatted raw terminal data variables into structured JSON objects to replicate industry-standard sensor packets.

May 25, 2026 — Phase 1: Local Server and Simulation Sandbox
Milestone: Initialized the baseline project directories and isolated software layers.
Technical Updates:
Set up a working Node.js web environment with Express running locally on port 3000.
Wrote a basic Python simulation script using normal loops and the native random library to generate varying temperature and speed numbers
