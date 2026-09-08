from fastapi import FastAPI
from app.core.config import Settings
from app.core.http import create_app
from app.features.finlit.ai_skills import LOCAL_SKILLS
from app.features.finlit.routers import router as feature_router
from app.settings import AppSettings

def build_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or AppSettings.from_env()
    return create_app(
        settings, extra_routers=[feature_router], local_skills=LOCAL_SKILLS
    )

app = build_app()
