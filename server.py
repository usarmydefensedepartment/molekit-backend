from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory store for simplicity
logs = []

@app.route("/submit", methods=["POST"])
def submit():
    # Expect JSON payload from Shortcut
    data = request.get_json()
    logs.append(data)
    return jsonify({"status": "received", "entries": len(logs)})

@app.route("/logs", methods=["GET"])
def get_logs():
    # Return all collected data
    return jsonify(logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
