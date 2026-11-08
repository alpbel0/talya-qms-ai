"""Onay kuyruğu — PLANLANDI. Uygulama yok; uç 501 döndürür."""

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["review"])


@router.get("/review-queue")
def get_review_queue() -> None:
    # planlandı: Onay kuyruğu
    raise HTTPException(status_code=501, detail="Planlandı: henüz uygulanmadı")
