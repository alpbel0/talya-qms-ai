"""DÖF (düzeltici/önleyici faaliyet) önerisi — PLANLANDI. Uygulama yok; uç 501 döndürür."""

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["recommendations"])


@router.post("/recommendations")
def create_recommendation() -> None:
    # planlandı: DÖF (düzeltici/önleyici faaliyet) önerisi
    raise HTTPException(status_code=501, detail="Planlandı: henüz uygulanmadı")
