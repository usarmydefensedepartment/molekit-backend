from flask import Flask, request, jsonify, send_file
import json
import os

app = Flask(__name__)
LOG_FILE = "logs.json"

# Initialize log file if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

def load_logs():
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    logs = load_logs()
    logs.append(data)
    save_logs(logs)
    return jsonify({"status": "received", "total_entries": len(logs)})

@app.route("/logs", methods=["GET"])
def get_logs():
    logs = load_logs()
    limit = request.args.get("limit", type=int)
    device_filter = request.args.get("device")

    if device_filter:
        logs = [log for log in logs if device_filter.lower() in log.get("device_name", "").lower()]
    if limit:
        logs = logs[-limit:]

    return jsonify(logs)

@app.route("/download", methods=["GET"])
def download_logs():
    return send_file(LOG_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
