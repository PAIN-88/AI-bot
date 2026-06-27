from groq import Groq
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask,request,jsonify
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
load_dotenv()

app = Flask(__name__)
CORS(app) 
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

#Load Vectorstore data

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
       persist_directory = "vectorstore",
       embedding_function = embeddings
)

@app.route("/chat", methods=["POST"])
def chat():
          
          #User Message
          user_message = request.json.get("message")

          #Search Chunks according to user message
          docs = vectorstore.similarity_search(user_message, k=3)
          context = "\n".join([doc.page_content for doc in docs])

          #Give Extracted content + question of User to Groq
          response = client.chat.completions.create(
              model="llama-3.3-70b-versatile",
              
              messages=[
                  {
            "role": "system",
            "content": f"""You are a KIPM COLLEGE OF ENGINEERING AND TECHNOLOGY policy and detail assistant. Answer questions based on KIPM  policy and detail documents only.
            
            Context:
            {context}"""        },

                                {"role": "user", "content": user_message}
              ]
          )
      
          bot_reply =  response.choices[0].message.content
          return jsonify({"reply":bot_reply})

if __name__ == "__main__":
    app.run(debug=True,port=500)
