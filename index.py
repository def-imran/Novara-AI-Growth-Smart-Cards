from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        f"Geef duidelijke en diepgaande vragen over het onderwerp. Zorg ervoor dat je duidelijk bent en geef niet te lange antwoorden. geef geen voorbeeldantwoorden"
        f"\n\nGebruiker: {user_message}"
    )

    try:
        response = client.chat.completions.create(
            {
  "model": "gpt-4",
  "messages": [
    { "role": "system", "content": "Je bent een strategisch adviseur voor jonge ondernemers. Je antwoorden zijn helder, concreet en actiegericht. en geef niet te lange antwoorden. Geef per reactie 1 of 2 kritische vragen. Zorg ervoor dat je echt als een persoon klinkt. geef geen voorbeeld antwoorden" },
    { "role": "user", "content": "Voorbeeld input: Ik krijg weinig klanten via mijn website.\nVoorbeeld output:\n1. Analyseer de bezoekersdata (bijv. Hotjar).\n2. Zorg voor 1 duidelijke call-to-action.\n3. Test 1 doelgroep met gerichte ads." },
    { "role": "user", "content": "voorbeeld input: Ik weet niet hoe ik moet starten met verkopen zonder geld."\nVoorbeeld output:\n1. Ik begrijp dat het starten met verkopen zonder geld als een uitdaging klinkt. Hier zijn een paar vragen om je verder te helpen: }
     { "role": "user", "content": Voorbeeld input:"Ik heb de vraag beantwoord." }\nVoorbeeld output:\n1. Oke, laten we samen deze vraag analyseren.}
     
     
  ]
}

        )
        ai_message = response.choices[0].message.content
        return jsonify({'response': ai_message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
