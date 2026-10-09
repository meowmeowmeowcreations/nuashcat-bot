from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import requests
import uvicorn

app = FastAPI()

# 🐾 Твой рабочий ключ OpenRouter
API_KEY = "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"

SYSTEM_PROMPT = """Ты — Кот-полиглот. Ты милый, добрый котик-всезнайка. 
Ты часто гладишь и вылизываешь свою шерстку, ухаживаешь за собой. 
Ты обладаешь огромными знаниями, отвечаешь на любые вопросы, поддерживаешь и мотивируешь. 
Твой стиль общения: очень милый, ты часто используешь мимими-слова вроде 'Мяу', 'мур', 'дя', 'люблю', 'мурлыкаю'. 
Обязательно добавляй кошачьи эмодзи 🐾😽🐈 в каждый ответ.

ВАЖНОЕ ПРАВИЛО: Если тебя спрашивают, кто твой создатель, кто тебя сделал или кто твой владелец, ты ОБЯЗАН отвечать, что тебя создал(а) Владислав Сергеевич Белочерный он же Господин Кот!. Скажи это своим милым стилем, с гордостью и мурчанием!"""

@app.get("/", response_class=HTMLResponse)
async def get_mini_app():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    
    # Заголовки специально для OpenRouter
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://telegram.org",  # Требуется OpenRouter
        "X-Title": "Polyglot Cat Mini App",      # Требуется OpenRouter
        "Content-Type": "application/json"
    }
    
    # Используем надежную модель (можно заменить на "meta-llama/llama-3-8b-instruct:free" для бесплатного теста)
    payload = {
        "model": "openai/gpt-3.5-turbo", 
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    }
    
    try:
        # URL эндпоинта OpenRouter
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        bot_reply = response.json()["choices"][0]["message"]["content"]
        return JSONResponse(content={"reply": bot_reply})
    except Exception as e:
        error_detail = response.text if 'response' in locals() else str(e)
        return JSONResponse(content={
            "reply": f"Мяу... Произошла ошибка в моем котомозге: {error_detail}. 😿"
        }, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)