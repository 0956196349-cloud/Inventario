from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.inventario import InventarioCreate, InventarioResponse, DisminuirStockIn
from app.dao.inventario_dao import list_items, get_item, create_item, disminuir_stock

router = APIRouter()

@router.get("/")
def listar(db: Session = Depends(get_db)):
    items = list_items(db)
    return [InventarioResponse.model_validate(x).model_dump() for x in items]

@router.get("/{item_id}")
def obtener(item_id: int, db: Session = Depends(get_db)):
    obj = get_item(db, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Producto no existe")
    return InventarioResponse.model_validate(obj).model_dump()

@router.post("/")
def crear(data: InventarioCreate, db: Session = Depends(get_db)):
    obj = create_item(db, data.nombre, data.tipo, data.cantidad, data.estado)
    return InventarioResponse.model_validate(obj).model_dump()

@router.patch("/{item_id}/disminuir")
def patch_disminuir(item_id: int, body: DisminuirStockIn, db: Session = Depends(get_db)):
    obj, err = disminuir_stock(db, item_id, body.cantidad)
    if err == "Producto no existe":
        raise HTTPException(status_code=404, detail=err)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return InventarioResponse.model_validate(obj).model_dump()
