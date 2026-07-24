import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import analytics, events, health

app = FastAPI(
    title="F1 Race Intelligence API",
    description=(
        "REST API providing Formula 1 race results, " "lap data and analytics."
    ),
    version="1.0.0",
)


def get_allowed_origins() -> list[str]:
    configured_origins = os.getenv("ALLOWED_ORIGINS", "")

    production_origins = [
        origin.strip() for origin in configured_origins.split(",") if origin.strip()
    ]

    local_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    return local_origins + production_origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router)
app.include_router(events.router)
app.include_router(analytics.router)


FRONTEND_URL = os.getenv("FRONTEND_URL", "")


@app.get("/")
def root() -> dict[str, str]:
    response = {
        "name": "F1 Race Intelligence API",
        "status": "running",
        "documentation": "/docs",
    }

    if FRONTEND_URL:
        response["frontend"] = FRONTEND_URL

    return response
