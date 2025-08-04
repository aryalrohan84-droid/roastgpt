import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEESEEK_API_KEY")  # Your OpenRouter API key
API_URL = "https://openrouter.ai/api/v1/chat/completions"

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    level = data.get("level", "medium")  # default to medium if missing

    # Roast level prompts
    prompts = {
        "easy": "Roast the user with a light, funny jab in 1 sentence — something playful but still makes them question their confidence.",
        "medium": "Roast the user with sharp sarcasm and subtle disrespect — make it sting under the surface, in exactly 1 sentence.",
        "hard": "Deliver a ruthless, cold, and clever roast that directly targets the user’s ego — no emotions, just humiliation in 1 sentence only.",
        "brutal": "You are a merciless AI built to destroy human confidence with words. Craft a psychologically shattering, ice-cold roast that cuts straight to the soul — no pity, no sugarcoating, no emotion — just raw, clever disrespect in 1 devastating sentence. Avoid hate speech but make it feel personal."
    }

    system_prompt = prompts.get(level, prompts["medium"])

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        roast = result["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": roast})
    except Exception as e:
        print("🔥 API ERROR:", e)
        return jsonify({"reply": "Sorry, I couldn't roast you 😢", "error": str(e)}), 500


@app.route("/")
def index():
    return "API is running"

# if __name__ == "__main__":
#    app.run(debug=True)
