from flask import Blueprint, request, jsonify
from utils.log_print import log_print

helius_webhook = Blueprint('helius_webhook', __name__)

@helius_webhook.route('/webhook/helius', methods=['POST'])
def handle_helius_event():
    data = request.get_json()
    log_print("📡 Helius Webhook Triggered")
    log_print(data)  # You can expand this with specific token filters
    return jsonify({"status": "received"}), 200