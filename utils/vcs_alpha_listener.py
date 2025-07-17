
import sys, os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

from flask import Flask, request, jsonify
from utils.telegram_alerts import send_alert
import json

app = Flask(__name__)
ALPHA_LOG = os.path.join("logs", "vcs_calls.json")

@app.route("/vcs/signal", methods=["POST"])
def receive_signal():
    data = request.get_json()
    token = data.get("token")
    mint = data.get("mint")
    reason = data.get("reason", "VCS Alpha Call")

    if not token or not mint:
        return jsonify({"error": "Missing required fields"}), 400

    entry = {
        "token": token,
        "mint": mint,
        "reason": reason
    }

    try:
        if os.path.exists(ALPHA_LOG):
            with open(ALPHA_LOG) as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(entry)
        with open(ALPHA_LOG, 'w') as f:
            json.dump(logs, f, indent=2)

        alert_msg = f"📢 VCS Alpha Call: {token}\nMint: {mint}\nReason: {reason}"
        send_alert(alert_msg)

        return jsonify({"status": "success", "data": entry}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5050)
