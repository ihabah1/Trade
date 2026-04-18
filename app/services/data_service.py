import gspread
import requests
import os
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from google import genai

load_dotenv()

SHEET_ID = "1HbUqH2x6gdWKZVVF3whkEAD01VUAmms7nM5M_nnwTj8"

print("ENV GOOGLE_CREDS_JSON:", os.getenv("GOOGLE_CREDS_JSON")[:50] if os.getenv("GOOGLE_CREDS_JSON") else "NONE")
print("ENV GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))

# ---------------------------
# 📥 LOAD GOOGLE SHEET
# ---------------------------
def load_data():
    print("\n📥 LOADING GOOGLE SHEET...")

    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        creds_json = os.getenv("GOOGLE_CREDS_JSON")

        if not creds_json:
            print("❌ NO GOOGLE_CREDS_JSON")
            return [], []

        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)

        print("✅ SHEET CONNECTED")

        assets = sheet.worksheet("assets").get_all_records()
        sources = sheet.worksheet("sources").get_all_records()

        print("📊 ASSETS:", assets)
        print("📰 SOURCES:", sources)

        return assets, sources

    except Exception as e:
        print("❌ SHEET ERROR:", e)
        return [], []


# ---------------------------
# 📈 PRICES
# ---------------------------
def get_prices(assets):
    print("\n📈 FETCHING PRICES...")

    data = {}
    headers = {"User-Agent": "Mozilla/5.0"}

    for row in assets:
        symbol = row.get("symbol")
        name = row.get("name")

        print(f"👉 {name} ({symbol})")

        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            res = requests.get(url, headers=headers, timeout=5)

            print("STATUS:", res.status_code)

            if res.status_code != 200:
                data[name] = "—"
                continue

            json_data = res.json()
            price = json_data["chart"]["result"][0]["meta"]["regularMarketPrice"]

            print(f"💰 {name} = {price}")

            data[name] = price

        except Exception as e:
            print("❌ PRICE ERROR:", e)
            data[name] = "—"

    return data


def get_top_stocks():
    print("\n🏆 FETCHING TOP STOCKS...")

    # 🔥 fallback קבוע במקום API בעייתי
    return {
        "AAPL": 180,
        "MSFT": 420,
        "NVDA": 900,
        "AMZN": 170,
        "GOOGL": 150
    }
# ---------------------------
# 📰 NEWS
# ---------------------------
def get_news(sources):
    print("\n📰 LOADING NEWS...")

    news = []

    for src in sources:
        url = src.get("url")
        name = src.get("name")

        print(f"👉 {name} ({url})")

        try:
            res = requests.get(url, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")

            count = 0

            for tag in soup.find_all("h2"):
                text = tag.get_text(strip=True)

                if text and len(text) > 20:
                    news.append({
                        "title": text,
                        "url": url,
                        "source": name
                    })
                    count += 1

                if count >= 3:
                    break

        except Exception as e:
            print("❌ NEWS ERROR:", e)

    print("📰 NEWS RESULT:", news)

    return news


# ---------------------------
# 🧠 AI SUMMARY (NEW SDK)
# ---------------------------
def summarize_news(news):
    print("\n🧠 AI SUMMARY...")

    api_key = os.getenv("GOOGLE_API_KEY")

    print("🔑 API KEY:", api_key)

    if not api_key:
        print("❌ NO API KEY")
        return fallback(news)

    try:
        client = genai.Client(api_key=api_key)

        results = []

        for item in news[:5]:
            print(f"👉 AI: {item['title']}")

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
                כתבה:
                {item['title']}

                תן סיכום בעברית ב-2 משפטים בלבד.
                """
            )

            text = response.text or "אין סיכום"

            results.append({
                "title": item["title"],
                "summary": text.strip(),
                "url": item["url"],
                "source": item["source"],
                "date": "היום"
            })

        print("🧠 AI RESULT:", results)

        return results

    except Exception as e:
        print("❌ AI ERROR:", e)
        return fallback(news)


# ---------------------------
# 🛟 FALLBACK
# ---------------------------
def fallback(news):
    print("⚠️ USING FALLBACK")

    return [
        {
            "title": n["title"],
            "summary": "אין סיכום כרגע",
            "url": n["url"],
            "source": n["source"],
            "date": "היום"
        }
        for n in news
    ]


# ---------------------------
# 🚀 MAIN
# ---------------------------
def build_lobby_data():
    print("\n⚡ BUILDING DATA...")

    assets, sources = load_data()

    if not assets:
        print("❌ NO ASSETS")
    if not sources:
        print("❌ NO SOURCES")

    prices = get_prices(assets)
    top = get_top_stocks()
    news = get_news(sources)
    summary = summarize_news(news)

    data = {
        "prices": prices,
        "top": top,
        "news": news,
        "summary": summary
    }

    print("\n📦 FINAL DATA:", data)

    return data