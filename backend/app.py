from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

app = Flask(__name__)
CORS(app)

client = Groq(api_key=api_key)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    user_input = data.get("message")
    goal = data.get("goal")
    strength = data.get("strength")

    if not user_input:
        return jsonify({"reply": "Please enter a message"}), 400

    prompt = f"""
    You are a Personalized AI Decision Simulator Agent.

    User Profile:
    Goal: {goal}
    Strength: {strength}

    Task:
    1. Identify choices
    2. Simulate outcomes
    3. Compare options
    4. Give score out of 10
    5. Recommend best option

    Decision: {user_input}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = "Error occurred. Try again."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)