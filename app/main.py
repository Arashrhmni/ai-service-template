from fastapi import FastAPI

from app.routes import health

app = FastAPI(title="AI Service Template", version="0.1.0")

app.include_router(health.router)


@app.get("/")
async def root():
    return {"status": "ok", "service": "ai-service-template", "day": 2}