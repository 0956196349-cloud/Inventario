from pydantic import BaseModel, Field

class InventarioCreate(BaseModel):
    nombre: str = Field(min_length=1)
    tipo: str = Field(min_length=1)
    cantidad: int = Field(ge=0)
    estado: str = Field(min_length=1)

class InventarioResponse(BaseModel):
    id: int
    nombre: str
    tipo: str
    cantidad: int
    estado: str

    class Config:
        from_attributes = True

class DisminuirStockIn(BaseModel):
    cantidad: int = Field(gt=0)
