
from flask import Flask, render_template_string, jsonify, request
import json
import os
from datetime import datetime
import logging
import subprocess
import signal
from functools import wraps
from flask import Response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Remove backend endpoints for bot control
# Remove: /start-bot, /stop-bot, /bot-status, and bot_process global

# TODO: Add basic authentication for production deployment

def check_auth(username, password):
    return username == os.environ.get('DASHBOARD_USER', 'admin') and password == os.environ.get('DASHBOARD_PASS', 'admin')

def authenticate():
    return Response(
        'Authentication required', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/")
@requires_auth
def dashboard():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Memecoin Bot Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 100%;
            margin: 0 auto;
        }
        h1 {
            color: #00ff88;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 0 0 10px rgba(0,255,136,0.3);
        }
        .status-bar {
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #333;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #00ff88;
            margin-right: 10px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: rgba(0,0,0,0.4);
            border: 1px solid #333;
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        .card h3 {
            color: #00ff88;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        pre {
            background: rgba(0,0,0,0.6);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #444;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.4;
            max-height: 400px;
            overflow-y: auto;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: rgba(0,255,136,0.1);
            border: 1px solid #00ff88;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #00ff88;
        }
        .stat-label {
            color: #aaa;
            font-size: 0.9em;
        }
        .refresh-time {
            text-align: center;
            color: #666;
            font-size: 0.8em;
            margin-top: 20px;
        }
        .card.full-width {
            grid-column: 1 / -1;
        }
        .terminal-scan-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .terminal-scan-card {
            background: rgba(0,0,0,0.4);
            border: 1px solid #333;
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
            height: auto%;
            display: flex;
            flex-direction: column;
        }
        #terminal-log {
            background: rgba(0,0,0,0.85);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #444;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 1em;
            line-height: 1.5;
            min-height:5%;
            max-height: 50vh;
            color: #00ff88;
            margin: 0;
            width: 100%;
            box-sizing: border-box;
            flex: 1 1 auto;
        }
        .scan-iframe {
            width: 100%;
            min-height: 400px;
            height: 70vh;
            border: none;
            border-radius: 8px;
            background: #111;
        }
        #new-tokens {
            background: rgba(0,0,0,0.85);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #444;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 1em;
            line-height: 1.5;
            min-height: 400px;
            max-height: 70vh;
            color: #00ff88;
            margin: 0;
            width: 100%;
            box-sizing: border-box;
            flex: 1 1 auto;
        }
        @media (max-width: 1200px) {
            .grid {
                grid-template-columns: 1fr;
            }
            h1 {
                font-size: 2em;
            }
            #terminal-log, .scan-iframe, #new-tokens {
                min-height: 250px;
                height: 40vh;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Memecoin Bot Dashboard</h1>

        <div class="status-bar">
            <span class="status-indicator"></span>
            <strong>Bot Status:</strong> <span id="bot-status">Running</span>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="total-trades">0</div>
                <div class="stat-label">Total Trades</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="total-flags">0</div>
                <div class="stat-label">MEV Flags</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="active-tokens">0</div>
                <div class="stat-label">Active Tokens</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="profit-loss">$0.00</div>
                <div class="stat-label">P&L</div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>📊 Recent Trades</h3>
                <pre id="trades">Loading trades...</pre>
            </div>

            <div class="card">
                <h3>🚨 MEV Alerts</h3>
                <pre id="flags">Loading alerts...</pre>
            </div>
        </div>
        <div class="terminal-scan-grid">
            <div class="terminal-scan-card">
                <h3>🖥️ Terminal Output (Live)</h3>
                <pre id="terminal-log">Loading terminal output...</pre>
            </div>
        </div>

        <div class="refresh-time">
            Last updated: <span id="last-update">Never</span>
        </div>
    </div>

    <script>
        let updateCount = 0;

        async function fetchData() {
            try {
                const [tradeRes, flagRes, statusRes] = await Promise.all([
                    fetch('/logs/trades'),
                    fetch('/logs/mev'),
                    fetch('/status')
                ]);

                const trades = await tradeRes.json();
                const flags = await flagRes.json();
                const status = await statusRes.json();

                // Update trades
                document.getElementById("trades").textContent =
                    JSON.stringify(trades.slice(-10), null, 2);

                // Update flags
                document.getElementById("flags").textContent =
                    JSON.stringify(flags.slice(-10), null, 2);

                // Update stats
                document.getElementById("total-trades").textContent = trades.length;
                document.getElementById("total-flags").textContent = flags.length;
                document.getElementById("active-tokens").textContent = status.active_tokens || 0;
                document.getElementById("profit-loss").textContent = status.profit_loss || "$0.00";

                // Update bot status
                document.getElementById("bot-status").textContent = status.status || "Running";

                // Update last refresh time
                const now = new Date();
                document.getElementById("last-update").textContent =
                    now.toLocaleTimeString();

                updateCount++;

            } catch (error) {
                console.error('Error fetching data:', error);
                document.getElementById("bot-status").textContent = "Connection Error";
            }
        }

        async function fetchTerminalLog() {
            try {
                const res = await fetch('/logs/terminal');
                const text = await res.text();
                document.getElementById("terminal-log").textContent = text;
            } catch (e) {
                document.getElementById("terminal-log").textContent = "Error loading terminal log.";
            }
        }

        // Remove updateBotStatus, start/stop button logic, and related intervals

        // Initial load
        fetchData();

        // Auto-refresh every 5 seconds
        setInterval(fetchData, 5000);
        // Auto-refresh terminal log every 5 seconds
        setInterval(fetchTerminalLog, 5000);
        // Remove updateBotStatus();

        // Manual refresh on page focus
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                fetchData();
                fetchTerminalLog(); // Also refresh terminal log on page focus
            }
        });
    </script>
</body>
</html>
""")

@app.route("/logs/trades")
def trades():
    path = os.path.join(LOG_DIR, "trade_logs.json")
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return jsonify(data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Could not load trade logs: {e}")
        return jsonify([])
    except Exception as e:
        logger.error(f"Error loading trade logs: {e}")
        return jsonify([])

@app.route("/logs/mev")
def mev():
    path = os.path.join(LOG_DIR, "mev_flags.json")
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return jsonify(data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Could not load MEV flags: {e}")
        return jsonify([])
    except Exception as e:
        logger.error(f"Error loading MEV flags: {e}")
        return jsonify([])

@app.route("/logs/terminal")
def terminal_log():
    log_path = os.path.join(LOG_DIR, "terminal_output.log")
    try:
        if not os.path.exists(log_path):
            return "No terminal output yet.", 200, {"Content-Type": "text/plain"}
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_100 = lines[-100:] if len(lines) > 100 else lines
            return "".join(last_100), 200, {"Content-Type": "text/plain"}
    except Exception as e:
        logger.error(f"Error reading terminal log: {e}")
        return f"Error reading log: {e}", 500, {"Content-Type": "text/plain"}

@app.route("/status")
def status():
    """Return bot status information"""
    try:
        # Check if bot is running by looking for recent log files
        trade_path = os.path.join(LOG_DIR, "trade_logs.json")
        mev_path = os.path.join(LOG_DIR, "mev_flags.json")

        active_tokens = 0
        profit_loss = "$0.00"

        # Count recent trades (last 24 hours)
        if os.path.exists(trade_path):
            with open(trade_path, 'r') as f:
                trades = json.load(f)
                active_tokens = len(set(trade.get('token', '') for trade in trades[-50:]))

        return jsonify({
            "status": "Running",
            "active_tokens": active_tokens,
            "profit_loss": profit_loss,
            "last_update": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({
            "status": "Error",
            "active_tokens": 0,
            "profit_loss": "$0.00",
            "last_update": datetime.now().isoformat()
        })

@app.route("/health")
def health():
    """Health check endpoint for hosting providers"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
