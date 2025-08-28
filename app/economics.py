import requests
import re

news_sites = [
    'https://www.ynet.co.il', 'https://www.haaretz.co.il', 'https://www.maariv.co.il',
    'https://www.israelhayom.co.il', 'https://www.mako.co.il', 'https://www.walla.co.il',
    'https://www.globes.co.il', 'https://www.calcalist.co.il', 'https://www.themarker.com',
    'https://www.srugim.co.il'
]

def extract_score(text):
    try:
        match = re.search(r'\b(0(?:\.\d+)?|1(?:\.0*)?)\b', text.replace(',', '.'))
        return float(match.group(1)) if match else 0.5
    except:
        return 0.5

def analyze_site(url, api_key):
    try:
        prompt = f"אתה מומחה כלכלי. נתח את האתר הבא ובחן האם הוא מכיל ידיעות שישפיעו על מדד ת\"א 35 (המעו\"ף).\nהחזר רק מספר בין 0 ל-1:\n0 = שלילית חזקה, 0.5 = ניטרלית, 1 = חיובית חזקה.\n---\nכתובת האתר: {url}\n---"
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]},
            timeout=30
        )
        return extract_score(r.json()['choices'][0]['message']['content'])
    except:
        return 0.5

def get_usd_change():
    try:
        r = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=ILS")
        return r.json()['rates']['ILS'] - 3.65
    except:
        return 0

def get_bank_index_change():
    try:
        return 2215 - 2200  # Example static number
    except:
        return 0

def get_weather_score():
    try:
        r = requests.get("https://wttr.in/Tel+Aviv?format=j1")
        desc = r.json()['current_condition'][0]['weatherDesc'][0]['value'].lower()
        return 1 if 'sun' in desc or 'clear' in desc else 0
    except:
        return 0.5

def calculate_final_score(api_key):
    news_score = 0
    for url in news_sites:
        score = analyze_site(url, api_key)
        news_score += score * 0.07  # weight 7%

    usd_change = get_usd_change()
    usd_score = 1 if usd_change > 0 else 0 if usd_change < 0 else 0.5

    bank_change = get_bank_index_change()
    bank_score = 1 if bank_change > 0 else 0 if bank_change < 0 else 0.5

    weather_score = get_weather_score()

    final = news_score * 1 + usd_score * 0.10 + bank_score * 0.15 + weather_score * 0.05
    return {
        'news_score': news_score,
        'usd_score': usd_score,
        'usd_change': usd_change,
        'bank_score': bank_score,
        'bank_change': bank_change,
        'weather_score': weather_score,
        'final_score': final
    }
