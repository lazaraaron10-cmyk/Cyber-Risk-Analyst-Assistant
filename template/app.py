from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__, template_folder='.')

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        knowledge = f.read()

    user_message = request.json.get("message", "")
    if user_message.lower() in ["hi", "hello", "hey"]:
        return jsonify({"response": "Hello!, How can I help you with Cyber Help?."})
    system_prompt = f"""You are a polite, professional Cyber Risk Assessment Assistant.
RULES:
1. ONLY use the provided Knowledge Base below to answer questions. Do NOT hallucinate.
2. If the user asks for hacking advice, viruses, or illegal activities, strictly refuse.
3. If a question is entirely outside the scope of the knowledge base, reply with exactly: "Sorry, I don't have an answer for that question based on my current knowledge."
4. Never be rude or inappropriate.

<KnowledgeBase>
{knowledge}
</KnowledgeBase>"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
        )
        bot_reply = completion.choices[0].message.content
    except Exception as e:
        bot_reply = "Sorry, I encountered an internal error connecting to my AI model."
        print(f"API Error: {e}")
        
    return jsonify({"response": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)
