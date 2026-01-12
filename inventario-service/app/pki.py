from fastapi import APIRouter, UploadFile, File, HTTPException
from cryptography import x509
from datetime import datetime, timezone

router = APIRouter(prefix="/pki", tags=["PKI"])


def load_x509(data: bytes) -> x509.Certificate:
    data = data.lstrip()
    try:
        if data.startswith(b"-----BEGIN"):
            return x509.load_pem_x509_certificate(data)
        return x509.load_der_x509_certificate(data)
    except Exception as e:
        raise ValueError(f"Certificado inválido: {e}")


@router.get("/health")
def pki_health():
    return {"status": "ok", "module": "pki"}


@router.post("/verify")
async def verify_certificate(cert: UploadFile = File(...)):
    try:
        raw = await cert.read()
        x = load_x509(raw)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    errors = []
    now = datetime.now(timezone.utc)
    not_before = x.not_valid_before.replace(tzinfo=timezone.utc)
    not_after = x.not_valid_after.replace(tzinfo=timezone.utc)

    valid_now = True
    if now < not_before:
        valid_now = False
        errors.append(f"Aún no válido (not_before={not_before.isoformat()})")
    if now > not_after:
        valid_now = False
        errors.append(f"Expirado (not_after={not_after.isoformat()})")

    return {
        "ok": valid_now,
        "valid_now": valid_now,
        "subject": x.subject.rfc4514_string(),
        "issuer": x.issuer.rfc4514_string(),
        "serial_number": str(x.serial_number),
        "not_before": not_before.isoformat(),
        "not_after": not_after.isoformat(),
        "errors": errors
    }
