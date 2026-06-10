# 🏭 Industrial Predictive Maintenance Data Pipeline

An end-to-end telemetry analytics workflow designed to ingest, store, and track real-time industrial machinery sensor data (temperature, vibration, and rotational speed) to help predict equipment breakdown risks.

---

## 🧸 The Project Explained Simply (The Toy Factory Story)

Imagine a giant factory with an expensive **Toy-Making Robot** (`MAC-001`). If this robot breaks down, production stops and money is lost. To prevent this, we built a 3-part smart monitoring system:

1. **The Robot's Doctors (Python Simulator):** We attached electronic sensors to the robot. Every second, they measure its Temperature, Vibration, and Speed, shouting out what they see.
2. **The Mail Carrier (Node.js Server):** The sensors bundle these numbers into an envelope and send it over the local network to our Node.js server. The server catches it and says, *"Got it! Status 201!"*
3. **The Factory Diary (PostgreSQL Database):** The server immediately writes these numbers down as a permanent line inside a huge digital diary. 

**The Ultimate Goal:** By saving hundreds of lines of historical data (both normal conditions and overheating anomalies), we can eventually train an AI brain to read this diary, recognize failure patterns, and warn us *before* the robot breaks down!

---

## ⚙️ Architecture & Tech Stack

* **Frontend Documentation:** Markdown (`README.md`)
* **Data Ingestion API:** Node.js with Express framework
* **Telemetry Generation Engine:** Python 3 (using `requests` and `random` libraries)
* **Relational Storage Engine:** PostgreSQL Database with composite performance indexes

---

## 🚀 How To Run It Locally

### 1. Database Configuration
Open **pgAdmin** and execute this script inside your query tool to set up the data vault:

```sql
CREATE TABLE telemetry (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(50),
    temperature NUMERIC(5, 2),
    vibration NUMERIC(5, 2),
    rotational_speed NUMERIC(6, 1),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index created to optimize high-speed time-series lookups
CREATE INDEX idx_telemetry_machine_time ON telemetry (machine_id, timestamp DESC);


---

## 🗓 Project Development Timeline & Changelog

This log captures the incremental development phases of the predictive maintenance framework, tracking milestones from local script simulation to unified multi-language database logging.

### 🔹 June 08, 2026 — Phase 3: PostgreSQL Database Integration & Ingestion
* **Milestone:** Connected the Node.js API layer to a permanent relational PostgreSQL database layer (`predictive_maintenance`).
* **Technical Updates:**
  * Configured connection pooling using the `pg` native driver inside `server.js`.
  * Designed SQL database schemas for the `telemetry` dataset using standard data constraint formatting (`NUMERIC`, `SERIAL`).
  * Optimized search queries by executing a composite performance index (`idx_telemetry_machine_time`) on target query criteria (`machine_id`, `timestamp DESC`).
  * Secured production credentials by isolating environmental secrets inside local `.env` runtime configurations.

### 🔹 June 06, 2026 — Phase 2: Async Cross-Language Data Pipeline Link
* **Milestone:** Established an active local network bridge connecting the Python runtime environment to the Node.js runtime backend.
* **Technical Updates:**
  * Installed and implemented the Python `requests` network client to handle concurrent socket actions.
  * Transformed raw script printouts into structured, industry-standard JSON telemetry packets (`machine_id`, `temperature`, `vibration`, `rotational_speed`).
  * Successfully handled network handshakes via an Express API destination routing to `POST /api/telemetry`, yielding verifiable `201 Created` transmission statuses.

### 🔹 June 02, 2026 — Phase 1: Local Server & Script Sandbox Setup
* **Milestone:** Initialized the isolated decoupled software architecture.
* **Technical Updates:**
  * Created a functional web environment backend leveraging Node.js and the Express framework listening securely on local port `3000`.
  * Scripted an automated sequential simulation program in Python utilizing native loops and pseudo-random variance libraries to emulate realistic factory hardware readings.