from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "WNR Script API is running in debug mode."

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        print(">>> /generate called")
        print("Received data:", data)
        return jsonify({
            "station": data.get("station", "unknown"),
            "script": f"TEST SCRIPT GENERATED for topic: '{data.get('topic', 'no topic')}'. This proves your frontend → backend → UI loop works."
        })
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
