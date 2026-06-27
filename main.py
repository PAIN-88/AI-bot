from groq import Groq
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask,request,jsonify
load_dotenv()

app = Flask(__name__)
CORS(app) 
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

@app.route("/chat", methods=["POST"])
def chat():
      
      
          user_message = request.json.get("message")
      
          response = client.chat.completions.create(
              model="llama-3.3-70b-versatile",
              
              messages=[
                  {
            "role": "system",
            "content": "Always reply in structured format with bullet points and headings. Make your response easy to read and well organized."
        },
        {"role": "user", "content": user_message}
              ]
          )
      
          bot_reply =  response.choices[0].message.content
          return jsonify({"reply":bot_reply})

if __name__ == "__main__":
    app.run(debug=True,port=500)
