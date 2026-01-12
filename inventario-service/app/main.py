import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Microservicio Ventas - TIGO", version="1.0")

INVENTARIO_URL = os.getenv("INVENTARIO_URL", "https://inventario-qivs.onrender.com")


class VentaCreate(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(gt=0)


@app.get("/health")
def health():
    return {"status": "ok", "service": "ventas"}


@app.post("/ventas")
def crear_venta(venta: VentaCreate):
    try:
        r = requests.get(f"{INVENTARIO_URL}/inventario/{venta.producto_id}", timeout=15)
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="No se pudo conectar con Inventario")

    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="Producto no existe en Inventario")
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Inventario respondió con error")

    producto = r.json()
    stock = int(producto.get("cantidad", 0))

    if stock < venta.cantidad:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente. Stock actual: {stock}, solicitado: {venta.cantidad}"
        )

    try:
        r2 = requests.patch(
            f"{INVENTARIO_URL}/inventario/{venta.producto_id}/disminuir",
            json={"cantidad": venta.cantidad},
            timeout=15
        )
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Error al descontar stock en Inventario")

    if r2.status_code == 404:
        raise HTTPException(status_code=404, detail="Producto no encontrado al descontar stock")
    if r2.status_code == 400:
        try:
            detail = r2.json().get("detail", "Stock insuficiente")
        except Exception:
            detail = "Stock insuficiente"
        raise HTTPException(status_code=400, detail=detail)
    if r2.status_code != 200:
        raise HTTPException(status_code=502, detail="Inventario no pudo actualizar el stock")

    producto_actualizado = r2.json()

    return {
        "message": "Venta registrada y stock actualizado",
        "venta": {"producto_id": venta.producto_id, "cantidad": venta.cantidad},
        "producto_actualizado": producto_actualizado
    }
