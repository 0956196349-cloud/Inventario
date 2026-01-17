from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.routers.health import router as health_router
from app.routers.inventario import router as inventario_router
from app.routers.pki import router as pki_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Microservicio Inventario - TIGO", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(inventario_router, prefix="/inventario", tags=["Inventario"])
app.include_router(pki_router, prefix="/pki", tags=["PKI"])
