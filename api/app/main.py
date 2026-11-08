"""Talya QMS-AI API — iskelet.

Şu an yalnızca sağlık kontrolü uçu vardır. Diğer uçlar app/routers/ altında 501
(Not Implemented) döndüren yer tutucudur ve bilerek buraya BAĞLANMAMIŞTIR.
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def _cors_origins() -> list[str]:
    raw = os.getenv("API_CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
    return [o.strip() for o in raw.split(",") if o.strip()]


app = FastAPI(title="Talya QMS-AI API", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
