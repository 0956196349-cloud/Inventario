from fastapi import APIRouter, HTTPException
from app.schemas.pki import PkiVerifyIn, PkiVerifyOut
from app.security.pki_utils import verify_pem_certificate

router = APIRouter()

@router.post("/verify")
def verify(body: PkiVerifyIn):
    try:
        info = verify_pem_certificate(body.pem_cert)
        return PkiVerifyOut(
            ok=True,
            subject=info["subject"],
            issuer=info["issuer"],
            serial_number=info["serial_number"],
            not_before=info["not_before"],
            not_after=info["not_after"],
            message="Certificado válido (formato PEM leído correctamente)."
        ).model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Certificado inválido: {str(e)}")
