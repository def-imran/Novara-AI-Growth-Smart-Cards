from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Kaarten zonder group_questions, AI bedenkt ze zelf
cards = {
   
  "I-01": {
    "card_text": "Wat motiveert jou het meest om ergens hard aan te werken?",
    "theme": "motivatie"
  },
  "I-02": {
    "card_text":"Welke fout in je leven heeft je het meest geholpen om te groeien?",
    "theme": "groei"
  },
  "I-03": {
    "card_text": "Hoe ziet een goede balans tussen werk en privé eruit voor jou?",
    "theme": "balans"
  },
  "I-04": {
    "card_text": "Wat betekent vrijheid voor jou in je dagelijks leven?",
    "theme": "vrijheid"
  },

  "I-05": {
    "card_text": "Wanneer voel jij je het meest creatief?",
    "theme": "creativiteit"
  },

  "I-06": {
    "card_text": "Wat vind jij belangrijker: goed samenwerken of zelfstandigheid?",
    "theme": "maatschappij"
  },

  "I-07": {
    "card_text": "Wat zou je willen leren als je geen angst had om te falen?",
    "theme": "angst"
  },

  "I-08": {
    "card_text": "Wat maakt een dag voor jou echt geslaagd?",
    "theme": "succes"
  },

  "I-09": {
    "card_text": "Hoe ga jij om met kritiek van anderen?",
    "theme": "kritiek"
  },

  "I-10": {
    "card_text": "Welke droom zou je nog graag waarmaken?",
    "theme": "doelen"
  },

  "I-11": {
    "card_text": "Wat vind jij het leukste aan anderen helpen?",
    "theme": "hulpvaardigheid"
  },

  "I-12": {
    "card_text": "Wat zou je doen als geld geen rol speelde in je keuzes?",
    "theme": "geld"
  }
}
    # Voeg meer kaarten toe indien nodig


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

    # Samengestelde prompt: AI bedenkt groepsvragen en begeleidt de sessie
    kaart_prompt = (
        f"Je begeleidt een groepssessie rondom persoonlijke groei. "
        f"De kaartvraag is: '{card['card_text']}' (thema: {card['theme']}).\n"
        "1. Herhaal de kaartvraag.\n"
        "2. Bedenk 2 tot 3 diepgaande groepsvragen die aansluiten bij het thema en de kaartvraag.\n"
        "3. Geef daarna een kort, inspirerend voorbeeldantwoord op de kaartvraag.\n"
        "Wees uitnodigend en positief. Gebruik duidelijke opsommingstekens voor de groepsvragen."
        f"\n\nGebruiker: {user_message}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Je bent een warme, uitnodigende groepscoach die mensen begeleidt bij persoonlijke groei."},
                {"role": "user", "content": kaart_prompt}
            ]
        )
        ai_message = response['choices'][0]['message']['content']
        return jsonify({'response': ai_message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
