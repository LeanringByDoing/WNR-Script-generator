from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "WNR Script API is live."

@app.route("/generate", methods=["POST"])
def generate():
    return jsonify({"script": "Test response from live API."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
