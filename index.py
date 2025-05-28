from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import json

app = Flask(__name__)
CORS(app)

openai.api_key = "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"

# Voorbeeld kaarten dictionary, vervang eventueel door laden uit JSON-bestand
cards = {
    "038": {
        "card_text": "Waar lieg je tegen jezelf over?",
        "theme": "zelfbedrog",
        "group_questions": [
            "Wat herken je bij jezelf?",
            "Wat durf je vaak niet toe te geven?",
            "Wat is één stap in de andere richting?"
        ]
    } # Voeg meer kaarten toe indien nodig
}

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    card_id = data.get('cardId')
    user_message = data.get('message')

    if not card_id or not user_message:
        return jsonify({'error': 'cardId en message zijn verplicht'}), 400

    card = cards.get(card_id)
    if not card:
        return jsonify({'error': f'Kaart-ID {card_id} niet gevonden'}), 404

    # Stel de samengestelde prompt samen
    kaart_prompt = f"Kaartvraag: {card['card_text']}\n"
    if card.get('group_questions'):
        kaart_prompt += "Groepsvragen:\n"
        for q in card['group_questions']:
            kaart_prompt += f"- {q}\n"
    samengestelde_prompt = f"{kaart_prompt}\nGebruiker: {user_message}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Je bent een behulpzame AI-assistent."},
                {"role": "user", "content": samengestelde_prompt}
            ]
        )
        ai_message = response['choices'][0]['message']['content']
        return jsonify({'response': ai_message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
