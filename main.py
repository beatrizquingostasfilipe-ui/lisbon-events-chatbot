# main.py
import os
import json
import httpx
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from database.database import init_db
from api.routes import router

init_db()

app = FastAPI(
    title="🎉 Lisbon Events Chatbot API",
    description="API para descobrir eventos em Lisboa com um chatbot conversacional.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# ─── Chat Proxy ───────────────────────────────────────────────────────────────
class ChatMessage(BaseModel):
    message: str
    session_id: str
@app.post("/api/chat")
async def chat_proxy(body: ChatMessage):
    async with httpx.AsyncClient(timeout=60) as client:
        agents_res = await client.get("http://localhost:7778/v1/playground/agents")
        agent_id = agents_res.json()[0]["agent_id"]

        res = await client.post(
            f"http://localhost:7778/v1/playground/agents/{agent_id}/runs",
            data={"message": body.message, "session_id": body.session_id, "stream": "false", "monitor": "false"}
        )

        raw = res.text
        print("RAW COMPLETO:", raw[:500])

        try:
            obj = json.loads(raw)
            content = obj.get("content", raw)
            return {"reply": content}
        except Exception:
            return {"reply": raw}
# ─── Chat UI ──────────────────────────────────────────────────────────────────
@app.get("/chat", tags=["Chat UI"])
def chat_ui():
    path = os.path.join(os.path.dirname(__file__), "chat.html")
    return FileResponse(path)

# ─── Rota raiz ────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bem-vindo à Lisbon Events API! 🎉",
        "docs":    "http://localhost:8000/docs",
        "chat":    "http://localhost:8000/chat",
        "endpoints": {
            "eventos":      "GET /api/events",
            "seed":         "POST /api/etl/seed",
            "ticketmaster": "POST /api/etl/ticketmaster",
        },
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)