from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "WNR Script API with OpenAI + debug logging is live."

@app.route("/generate", methods=["POST"])
def generate():
    print(">>> /generate hit")
    try:
        data = request.json
        print("Payload received:", data)

        station_id = data.get("station")
        topic = data.get("topic")
        tone = {
            "humor": data.get("humor", 0.5),
            "absurdity": data.get("absurdity", 0.5),
            "investigative": data.get("investigative", 0.5)
        }
        lore_flags = data.get("lore", [])

        with open(f"stations/{station_id}.json") as f:
            station = json.load(f)

        anchor_names = ", ".join([a["name"] for a in station["anchors"]])
        reporter_names = ", ".join([r["name"] for r in station["reporters"]])
        lore_notes = "\n- " + "\n- ".join(station["lore"]) if lore_flags else ""
        special = "\n- " + "\n- ".join(station["station000_links"]) if "station000" in lore_flags else ""

        prompt = f"""You are writing a full fake news broadcast script for WNR Station {station['station_name']}.

Anchors: {anchor_names}
Reporters: {reporter_names}
Topic: {topic}
Tone: Humor={tone['humor']}, Absurdity={tone['absurdity']}, Investigative={tone['investigative']}

Station Lore:{lore_notes}
Station 000 Connections:{special}

Script format should include:
- [ANCHOR INTRO]
- [MAIN STORY]
- [FIELD REPORT]
- [ANCHOR RETURN]
- [CLOSING]

Each section should be 2–4 paragraphs and reflect character voice and tone settings.
"""

        print("Prompt to OpenAI:", prompt[:400] + "...")  # Trim for logs

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                { "role": "system", "content": "You are a WNR scriptwriter bot." },
                { "role": "user", "content": prompt }
            ],
            temperature=0.85,
            max_tokens=1600
        )

        script = response['choices'][0]['message']['content']
        print("OpenAI responded successfully. Returning script.")

        return jsonify({
            "station": station_id,
            "script": script
        })

    except Exception as e:
        print("ERROR during /generate:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
