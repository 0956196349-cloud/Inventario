import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Microservicio Ventas - TIGO", version="1.0")

INVENTARIO_URL = os.getenv("INVENTARIO_URL", "http://localhost:8000")

# “BD” en memoria (simple para demo)
SALES: List[Dict[str, Any]] = []

class SaleItem(BaseModel):
    item_id: int
    cantidad: int = Field(gt=0)

class SaleCreate(BaseModel):
    cliente: str
    items: List[SaleItem]

@app.get("/health")
def health():
    return {"status": "ok", "service": "ventas"}

@app.get("/ventas")
def listar_ventas():
    return SALES

@app.post("/ventas")
async def crear_venta(payload: SaleCreate):
    async with httpx.AsyncClient(timeout=10) as client:
        # 1) Validar stock consultando inventario
        for it in payload.items:
            r = await client.get(f"{INVENTARIO_URL}/inventario/{it.item_id}")
            if r.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Item {it.item_id} no existe en inventario")
            if r.status_code != 200:
                raise HTTPException(status_code=502, detail="Error consultando inventario")

            item = r.json()
            stock = item.get("cantidad", 0)

            if stock < it.cantidad:
                raise HTTPException(
                    status_code=400,
                    detail=f"Stock insuficiente para item {it.item_id}. Stock={stock}, solicitado={it.cantidad}"
                )

        # 2) Descontar stock en inventario
        for it in payload.items:
            r2 = await client.patch(
                f"{INVENTARIO_URL}/inventario/{it.item_id}/disminuir",
                json={"cantidad": it.cantidad},
            )
            if r2.status_code != 200:
                raise HTTPException(status_code=502, detail="No se pudo descontar stock en inventario")

    # 3) Guardar venta (en memoria)
    venta = {
        "id": len(SALES) + 1,
        "cliente": payload.cliente,
        "items": [i.dict() for i in payload.items],
        "fecha": datetime.utcnow().isoformat() + "Z",
    }
    SALES.append(venta)

    return {"message": "Venta creada", "venta": venta}
