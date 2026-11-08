"""CSV/Excel veri içe aktarma — PLANLANDI. Uygulama yok; uç 501 döndürür."""

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["imports"])


@router.post("/imports")
def create_import() -> None:
    # planlandı: CSV/Excel veri içe aktarma
    raise HTTPException(status_code=501, detail="Planlandı: henüz uygulanmadı")
