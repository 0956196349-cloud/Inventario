from pydantic import BaseModel

class InventarioBase(BaseModel):
    nombre: str
    tipo: str
    cantidad: int
    estado: str


class InventarioCreate(InventarioBase):
    pass


class InventarioResponse(InventarioBase):
    id: int

    class Config:
        from_attributes = True
