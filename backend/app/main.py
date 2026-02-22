from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.db.init_db import init_db
from backend.app.api.routes.controls import router as controls_router

app = FastAPI(
    title=settings.api_name,
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(controls_router, prefix="/api")

@app.get("/")
def root():
    return {"name": settings.api_name, "env": settings.env}

@app.get("/health")
def health():
    return {"status": "ok"}
