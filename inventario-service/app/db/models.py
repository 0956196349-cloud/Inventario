from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    tipo = Column(String(60), nullable=False)
    cantidad = Column(Integer, nullable=False, default=0)
    estado = Column(String(30), nullable=False, default="activo")
