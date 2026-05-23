from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Correct Target Server
TARGET_URL = "http://69.197.168.194:5000/bot/check"

# Required Headers
HEADERS = {
    "X-Web-Token": "8NklgANMsCsMcMvUz5ZsdQgdIDupy6-5Qr4-4vwcTNk",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; V2166 Build/SP1A.210812.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/148.0.7778.120 Mobile Safari/537.36",
    "Referer": "http://69.197.168.194:5000/"
}

# Home Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "Your Render API is running successfully!"
    }), 200


# Main API Route
@app.route('/bot/check', methods=['GET', 'POST'])
def check_card_api():

    card_param = None
    gate_param = "pp"

    # GET Request Handling
    if request.method == 'GET':
        card_param = request.args.get('card')
        gate_param = request.args.get('gate', 'pp')

    # POST Request Handling
    elif request.method == 'POST':

        # JSON Body
        if request.is_json:
            json_data = request.get_json()
            card_param = json_data.get('card')
            gate_param = json_data.get('gate', 'pp')

        # Form Data
        else:
            card_param = request.form.get('card')
            gate_param = request.form.get('gate', 'pp')

    # Validation
    if not card_param:
        return jsonify({
            "ok": False,
            "error": "Missing 'card' parameter"
        }), 400

    # Payload Forwarding
    payload = {
        "gate": gate_param,
        "card": card_param.strip(),
        "proxy": "",
        "site": ""
    }

    try:

        # Forward Request
        response = requests.post(
            TARGET_URL,
            headers=HEADERS,
            json=payload,
            timeout=25
        )

        # Try JSON Response
        try:
            return jsonify(response.json()), response.status_code

        except Exception:
            return jsonify({
                "ok": False,
                "error": "Target server returned non-JSON response",
                "raw": response.text
            }), 500

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": "Internal connection failed",
            "details": str(e)
        }), 500


# Render Deployment
if __name__ == '__main__':

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host='0.0.0.0',
        port=port
    )
