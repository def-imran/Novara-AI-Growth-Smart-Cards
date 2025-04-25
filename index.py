from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Voeg je OpenAI API-sleutel toe
openai.api_key = "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"  # Vervang dit door je eigen API-sleutel

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'Geen bericht ontvangen'}), 400

    try:
        # OpenAI API-aanroep
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Je bent een behulpzame AI-assistent."},
                {"role": "user", "content": user_message}
            ]
        )
        ai_message = response['choices'][0]['message']['content']
        return jsonify({'response': ai_message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)