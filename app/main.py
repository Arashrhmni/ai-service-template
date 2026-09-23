# app/main.py
from fastapi import FastAPI
from app.routes import health, items

app = FastAPI(title="AI Service Template", version="0.1.0")

app.include_router(health.router)
app.include_router(items.router)


@app.get("/")
async def root():
    return {"status": "ok", "service": "ai-service-template", "day": 4}