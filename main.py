from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Target Server Configuration
TARGET_URL = "http://69.197.168"

HEADERS = {
    "X-Web-Token": "8NklgANMsCsMcMvUz5ZsdQgdIDupy6-5Qr4-4vwcTNk",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; V2166 Build/SP1A.210812.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/148.0.7778.120 Mobile Safari/537.36",
    "Referer": "http://69.197.168"
}

# Root route to check if your API is alive on Render
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "Your private API is running successfully on Render!"
    }), 200

# Your requested endpoint: /bot/check
@app.route('/bot/check', methods=['GET', 'POST'])
def check_card_api():
    card_param = None
    gate_param = "pp"

    # 1. Handle GET Requests (e.g., URL parameters)
    if request.method == 'GET':
        card_param = request.args.get('card')
        gate_param = request.args.get('gate', 'pp')

    # 2. Handle POST Requests (JSON or Form submission)
    elif request.method == 'POST':
        if request.is_json:
            json_data = request.get_json()
            card_param = json_data.get('card')
            gate_param = json_data.get('gate', 'pp')
        else:
            card_param = request.form.get('card')
            gate_param = request.form.get('gate', 'pp')

    # Validation: If card parameter is completely missing
    if not card_param:
        return jsonify({
            "ok": False,
            "error": "Missing 'card' parameter. Use format: cc|mm|yy|cvv"
        }), 400

    payload = {
        "gate": gate_param,
        "card": card_param.strip(),
        "proxy": "",
        "site": ""
    }

    try:
        # Forwarding request to the underlying server
        response = requests.post(TARGET_URL, headers=HEADERS, json=payload, timeout=25)
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                "ok": False,
                "error": f"Target server responded with status {response.status_code}",
                "details": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": "Internal connection failed",
            "details": str(e)
        }), 500

# Production configuration block for Render environment
if __name__ == '__main__':
    # Render assigns a dynamic port number via environment variables.
    # This prevents 'Port Scan Timeout' and deployment failures.
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
