from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json

app = Flask(__name__)
CORS(app)

key = os.getenv("OPENAI_API_KEY")
openai.api_key = key
print("🔑 OpenAI API Key Present:", bool(key))
if key:
    print("🔑 Key starts with:", key[:8] + "..." if len(key) > 8 else key)

@app.route("/")
def home():
    return "WNR Script API (key check build)"

@app.route("/generate", methods=["POST"])
def generate():
    print(">>> /generate hit")
    try:
        data = request.json
        print("Payload received:", data)

        prompt = f"""Write a short WNR-style fake news segment for topic: {data.get('topic', 'no topic')}"""
        print("Sending to OpenAI...")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                { "role": "system", "content": "You write fake local news for WNR." },
                { "role": "user", "content": prompt }
            ],
            temperature=0.8,
            max_tokens=400
        )

        script = response['choices'][0]['message']['content']
        print("✅ Got response from OpenAI.")

        return jsonify({"script": script})

    except Exception as e:
        print("❌ ERROR during /generate:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
