import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.logging_conf import configure_logging
from app.middleware import RequestContextMiddleware
from app.rate_limit import RateLimitMiddleware
from app.routes import health, items

configure_logging()
log = structlog.get_logger()

app = FastAPI(title="AI Service Template", version="0.1.0")

app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestContextMiddleware)

app.include_router(health.router)
app.include_router(items.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    log.error(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        error_type=type(exc).__name__,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/")
async def root():
    return {"status": "ok", "service": "ai-service-template", "day": 6}
