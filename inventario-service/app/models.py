from sqlalchemy import Column, Integer, String
from app.database import Base

class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo = Column(String)
    cantidad = Column(Integer)
    estado = Column(String)
