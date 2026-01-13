from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router
from app.pki import router as pki_router  

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Microservicio Inventario - TIGO",
    version="1.0"
)

app.include_router(router)
app.include_router(pki_router)  

@app.get("/health")
def health():
    return {"status": "ok", "service": "inventario"}
