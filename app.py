import os
import json
from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

with open('instructions.txt', 'r') as file:
    system_instructions = file.read()

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain"
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=system_instructions
)

chat_history = []

def add_to_chat_history(role, content):
    chat_history.append({"role": role, "content": content})

def generate_response(user_input):
    add_to_chat_history("User", user_input)
    context = '\n'.join([f"{entry['role']} : {entry['content']}" for entry in chat_history])
    response = model.generate_content(context)
    response_text = response.candidates[0].content.parts[0].text
    add_to_chat_history("Assistant", response_text)
    return response_text

class DocumentStore:
    def __init__(self):
        self.documents = {}

    def index_documents(self, documents):
        for doc in documents:
            self.documents[doc["employee_id"]] = doc

    def retrieve_document(self, employee_id):
        return self.documents.get(employee_id, None)

document_store = DocumentStore()

with open('Details.json', 'r') as jsonfile:
    document_store.index_documents(json.load(jsonfile))

def normalize_string(s):
    return ' '.join(s.split()).lower()

software_mapping = {
    "ssms": "sql server management studio",
    "teams": "microsoft teams",
    "vs": "visual studio",
    "vs code": "visual studio code",
    "pm": "postman"
}

def map_software_name(name):
    normalized_name = normalize_string(name)
    return software_mapping.get(normalized_name, normalized_name)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    employee_id = data.get("employee_id")
    requested_software = map_software_name(data.get("requested_software"))

    if employee_id and requested_software:
        details = document_store.retrieve_document(employee_id)
        if details:
            permitted_software = [map_software_name(software) for software in details["access"]]
            if requested_software in permitted_software:
                response_text = generate_response(requested_software)
                return jsonify({"status": "success", "response": response_text})
            else:
                return jsonify({"status": "error", "message": "Software not permitted for the employee."})
        else:
            return jsonify({"status": "error", "message": "Invalid Employee ID."})
    else:
        return jsonify({"status": "error", "message": "Please enter both Employee ID and requested software."})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("user_input")
    if user_input:
        response_text = generate_response(user_input)
        return jsonify({"status": "success", "response": response_text})
    else:
        return jsonify({"status": "error", "message": "User input is required."})

if __name__ == '__main__':
    app.run(debug=True)
