"""Bilgi grafı üzerinde soru-cevap — PLANLANDI. Uygulama yok; uç 501 döndürür."""

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["qa"])


@router.post("/qa")
def ask_question() -> None:
    # planlandı: Bilgi grafı üzerinde soru-cevap
    raise HTTPException(status_code=501, detail="Planlandı: henüz uygulanmadı")
