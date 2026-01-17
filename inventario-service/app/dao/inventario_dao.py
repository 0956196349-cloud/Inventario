from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String

from app.db.database import Base

class InventarioItem(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    tipo = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False, default=0)
    estado = Column(String(30), nullable=False, default="activo")


def list_items(db: Session):
    return db.query(InventarioItem).order_by(InventarioItem.id.asc()).all()

def get_item(db: Session, item_id: int):
    return db.query(InventarioItem).filter(InventarioItem.id == item_id).first()

def create_item(db: Session, nombre: str, tipo: str, cantidad: int, estado: str):
    obj = InventarioItem(nombre=nombre, tipo=tipo, cantidad=cantidad, estado=estado)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def disminuir_stock(db: Session, item_id: int, cantidad: int):
    obj = get_item(db, item_id)
    if not obj:
        return None, "Producto no existe"
    if obj.cantidad < cantidad:
        return None, f"Stock insuficiente. Stock actual: {obj.cantidad}, solicitado: {cantidad}"
    obj.cantidad -= cantidad
    db.commit()
    db.refresh(obj)
    return obj, None
