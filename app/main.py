from fastapi import FastAPI

app = FastAPI(title="AI Service Template", version="0.1.0")


@app.get("/")
async def root():
    return {"status": "ok", "service": "ai-service-template", "day": 2}