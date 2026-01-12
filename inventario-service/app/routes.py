from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List

from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/inventario", tags=["Inventario"])
router = APIRouter(prefix="/pki", tags=["PKI"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class StockChange(BaseModel):
    cantidad: int = Field(gt=0, description="Cantidad mayor a 0")


class CertVerifyRequest(BaseModel):
    certificate_pem: str


@router.post("/", response_model=schemas.InventarioResponse)
def crear_item(item: schemas.InventarioCreate, db: Session = Depends(get_db)):
    nuevo = models.Inventario(**item.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/", response_model=List[schemas.InventarioResponse])
def listar_items(db: Session = Depends(get_db)):
    return db.query(models.Inventario).all()


@router.get("/{item_id}", response_model=schemas.InventarioResponse)
def obtener_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Inventario).filter(models.Inventario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item


@router.patch("/{item_id}/disminuir", response_model=schemas.InventarioResponse)
def disminuir_stock(item_id: int, payload: StockChange, db: Session = Depends(get_db)):
    item = db.query(models.Inventario).filter(models.Inventario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    if item.cantidad < payload.cantidad:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente. Stock actual: {item.cantidad}",
        )

    item.cantidad -= payload.cantidad
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{item_id}/aumentar", response_model=schemas.InventarioResponse)
def aumentar_stock(item_id: int, payload: StockChange, db: Session = Depends(get_db)):
    item = db.query(models.Inventario).filter(models.Inventario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    item.cantidad += payload.cantidad
    db.commit()
    db.refresh(item)
    return item


@router.post("/verify-certificate")
def verify_certificate(payload: CertVerifyRequest):
    try:
        cert = load_cert_from_pem(payload.certificate_pem)
    except Exception:
        raise HTTPException(status_code=400, detail="Certificado PEM inválido o corrupto.")

    checks = basic_cert_checks(cert)
    return {
        "valid": checks["ok"],
        "reason": checks.get("reason"),
        "info": cert_summary(cert),
    }