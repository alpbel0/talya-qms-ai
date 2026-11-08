"""Planlanan uçlar henüz uygulanmadı; hepsi 501 döndürmeli."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers import imports, qa, recommendations, review

app = FastAPI()
for module in (recommendations, qa, review, imports):
    app.include_router(module.router)

client = TestClient(app)


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("post", "/recommendations"),
        ("post", "/qa"),
        ("get", "/review-queue"),
        ("post", "/imports"),
    ],
)
def test_placeholder_returns_501(method, path):
    response = getattr(client, method)(path)
    assert response.status_code == 501
