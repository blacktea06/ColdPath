# Cold Path /chat proxy: keeps your Gemini API key on the server, never in the web page.
# Setup:   pip install fastapi uvicorn google-genai
# Run:     GEMINI_API_KEY=your_key uvicorn chat_proxy:app --port 8000
# Then in the app: Ask card > "Connect Gemini" > Backend URL = http://localhost:8000/chat
import json, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()
# Hackathon-open CORS. Restrict allow_origins to your real site before launch.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


class Req(BaseModel):
    system: str
    context: dict
    history: list = []
    message: str


@app.post("/chat")
def chat(r: Req):
    contents = [
        types.Content(role="user" if h["r"] == "me" else "model", parts=[types.Part(text=h["t"])])
        for h in r.history
    ]
    contents.append(types.Content(role="user", parts=[types.Part(text=r.message)]))
    out = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=r.system + "\n\nCONTEXT (live data, only source of truth):\n" + json.dumps(r.context),
            temperature=0.3,
            max_output_tokens=400,
        ),
    )
    return {"reply": out.text}


# ---- Optional: SMS alerts via Twilio (untested). pip install twilio ; set TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM ----
class Sms(BaseModel):
    to: str
    body: str


@app.post("/notify/sms")
def notify_sms(m: Sms):
    from twilio.rest import Client
    c = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])
    msg = c.messages.create(to=m.to, from_=os.environ["TWILIO_FROM"], body=m.body)
    return {"sid": msg.sid}
