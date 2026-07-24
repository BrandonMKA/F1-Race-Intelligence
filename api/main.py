from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import analytics, events, health


app = FastAPI(
    title="F1 Race Intelligence API",
    description=(
        "REST API providing Formula 1 race results, "
        "lap data and analytics."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


app.include_router(health.router)
app.include_router(events.router)
app.include_router(analytics.router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "F1 Race Intelligence API",
        "status": "running",
        "documentation": "/docs",
    }