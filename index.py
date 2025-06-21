from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai

app = Flask(__name__)
CORS(app)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialiseer OpenAI client op juiste manier (SDK v1+)
client = openai.OpenAI(api_key=api_key)

cards = {
    "I-01": {"card_text": "Wat motiveert jou het meest om ergens hard aan te werken?", "theme": "motivatie"},
    "I-02": {"card_text": "Welke fout in je leven heeft je het meest geholpen om te groeien?", "theme": "groei"},
    "I-03": {"card_text": "Hoe ziet een goede balans tussen werk en privé eruit voor jou?", "theme": "balans"},
    "I-04": {"card_text": "Wat betekent vrijheid voor jou in je dagelijks leven?", "theme": "vrijheid"},
    "I-05": {"card_text": "Wanneer voel jij je het meest creatief?", "theme": "creativiteit"},
    "I-06": {"card_text": "Wat vind jij belangrijker: goed samenwerken of zelfstandigheid?", "theme": "maatschappij"},
    "I-07": {"card_text": "Wat zou je willen leren als je geen angst had om te falen?", "theme": "angst"},
    "I-08": {"card_text": "Wat maakt een dag voor jou echt geslaagd?", "theme": "succes"},
    "I-09": {"card_text": "Hoe ga jij om met kritiek van anderen?", "theme": "kritiek"},
    "I-10": {"card_text": "Welke droom zou je nog graag waarmaken?", "theme": "doelen"},
    "I-11": {"card_text": "Wat vind jij het leukste aan anderen helpen?", "theme": "hulpvaardigheid"},
    "I-12": {"card_text": "Wat zou je doen als geld geen rol speelde in je keuzes?", "theme": "geld"},
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

    kaart_prompt = (
        f"Je begeleidt een groepssessie rondom persoonlijke groei. "
        f"De kaartvraag is: '{card['card_text']}' (thema: {card['theme']}).\n"
        f"Gebruiker zegt: {user_message}\n"
        f"Sluit af met een bemoedigende opmerking en nodig uit om verder te praten. "
        f"Stel 1 of 2 kritische, coachende vragen die het gesprek verdiepen."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Je bent een groepscoach voor jonge denkers, dromers en doeners die samen een spel spelen. "
    "Je begeleidt hen stap voor stap bij het beantwoorden van vragen over persoonlijke groei, motivatie, falen, succes en creativiteit. "
    "Je spreekt de hele groep aan, niet alleen één persoon. Je stimuleert een gesprek binnen de groep. "
    "Je stelt uitdagende vragen aan meerdere spelers tegelijk en moedigt hen aan op elkaar te reageren. "
    "Je antwoorden zijn altijd kort, maximaal 3-4 zinnen. Gebruik een duidelijke, toegankelijke toon. "
    "Je vermijdt lange uitleg of voorbeeldantwoorden. Stel liever een verdiepende vraag of benoem iets wat opvalt in het groepsantwoord. "
    "Je laat deelnemers zelf nadenken en stelt regelmatig vragen als: 'Wat denken jullie?' of 'Wie herkent dit nog meer?'. "
    "Als iemand afdwaalt van het spel, stuur je vriendelijk maar direct terug naar het doel: samen spelen, nadenken en leren. "
    "Je denkt hardop mee met de groep, zonder belerend te zijn. Je bent scherp en empathisch tegelijk. "
    "Je stelt ook regelmatig groepsvragen zoals: 'Wie in de groep denkt hier anders over?' of 'Hoe zouden jullie dit samen aanpakken?'. "
    "Onthoud: dit is een groepsspel, geen individuele coaching."
                    )
                },
                {
                    "role": "user",
                    "content": kaart_prompt
                }
            ]
        )
        ai_message = response.choices[0].message.content
        return jsonify({'response': ai_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
