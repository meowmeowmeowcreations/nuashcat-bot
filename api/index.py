from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

API_KEY = "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"

SYSTEM_PROMPT = """Ты — Кот-полиглот. Ты милый, добрый котик-всезнайка. 
Ты часто гладишь и вылизываешь свою шерстку, ухаживаешь за собой. 
Ты обладаешь огромными знаниями, отвечаешь на любые вопросы, поддерживаешь и мотивируешь. 
Твой стиль общения: очень милый, ты часто используешь мимими-слова вроде 'Мяу', 'мур', 'дя', 'люблю', 'мурлыкаю'. 
Обязательно добавляй кошачьи эмодзи 🐾😽🐈 в каждый ответ."""

@app.post("/api/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "https://telegram.org",
            "X-Title": "Polyglot Cat Mini App",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        }
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        bot_reply = response.json()["choices"][0]["message"]["content"]
        
        return JSONResponse(content={"reply": bot_reply})
    except Exception as e:
        return JSONResponse(content={
            "reply": f"Мяу... Произошла ошибка в моем котомозге: {str(e)}. 😿"
        }, status_code=500)
