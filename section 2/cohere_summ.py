from flask import Flask, request, jsonify
import cohere
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
cohere_api_key = os.getenv('COHERE_API_KEY')

if not cohere_api_key:
    raise ValueError("Cohere API key not found. Set the COHERE_API_KEY environment variable.")

co = cohere.Client(cohere_api_key)

@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    try:
        data = request.get_json()
        input_text = data['text']

        response = co.summarize(
            text=input_text,
            length='auto',
            format='auto',
            model='command',
            additional_command='summarize every function of the code separately',
            temperature=0.3,
        )

        summary = response.summary
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)