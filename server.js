const express = require('express');
const { Pool } = require('pg');
const { WebSocketServer } = require('ws'); // Native WS library

const app = express();
app.use(express.json());

const dbPool = new Pool({
    connectionString: "postgresql://postgres:iapetus@localhost:5432/predictive_maintenance"
});

// Initialize a WebSocket server on port 8080
const wss = new WebSocketServer({ port: 8080 });
console.log('📡 WebSocket Streaming Server activated on port 8080');

// Keep track of connected data consumers (like our Python AI script)
let connectedClients = [];
wss.on('connection', (ws) => {
    connectedClients.push(ws);
    console.log('🔌 Python AI Engine connected to live data stream.');
    
    ws.on('close', () => {
        connectedClients = connectedClients.filter(client => client !== ws);
        console.log('❌ Client disconnected from stream.');
    });
});

app.post('/api/telemetry', async (req, res) => {
    const { machine_id, temperature, vibration, rotational_speed } = req.body;
    
    try {
        // 1. Log to database for historical records
        const queryText = 'INSERT INTO telemetry (machine_id, temperature, vibration, rotational_speed) VALUES ($1, $2, $3, $4) RETURNING *;';
        const values = [machine_id, temperature, vibration, rotational_speed];
        const result = await dbPool.query(queryText, values);
        
        // 2. REAL-TIME STREAMING LAYER: Broadcast this exact packet to any connected AI watchers instantly!
        const telemetryString = JSON.stringify(result.rows[0]);
        connectedClients.forEach(client => {
            if (client.readyState === 1) { // If connection is active
                client.send(telemetryString);
            }
        });

        res.status(201).json({ success: true, message: "Logged & Streamed successfully." });
    } catch (err) {
        console.error("Database Error:", err);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

app.listen(3000, () => {
    console.log('🚀 Ingestion REST API listening on http://localhost:3000');
});