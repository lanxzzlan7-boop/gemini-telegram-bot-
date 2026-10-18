
import os
import requests
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GEMINI_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

offset = 0

while True:
    response = requests.get(
        URL + "getUpdates",
        params={"offset": offset, "timeout": 30},
        timeout=35
    ).json()

    for update in response.get("result", []):
        offset = update["update_id"] + 1
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

        if not chat_id or not text:
            continue

        if text == "/start":
            answer = "Halo! Gue AI bot lu, ayo ngobrol."
        else:
            try:
                result = model.generate_content(text)
                answer = result.text
            except Exception:
                answer = "Maaf, AI lagi bermasalah, coba lagi nanti."

        requests.post(
            URL + "sendMessage",
            json={"chat_id": chat_id, "text": answer},
            timeout=30
        )
