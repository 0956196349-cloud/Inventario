from fastapi import APIRouter, UploadFile, File, HTTPException
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timezone

router = APIRouter(prefix="/pki", tags=["PKI"])


def _load_cert(data: bytes) -> x509.Certificate:
    data = data.lstrip()
    try:
        if data.startswith(b"-----BEGIN"):
            return x509.load_pem_x509_certificate(data, default_backend())
        return x509.load_der_x509_certificate(data, default_backend())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Certificado inválido (PEM/DER): {e}")


@router.get("/health")
def pki_health():
    return {"status": "ok", "module": "pki"}


@router.post("/verify")
async def verify_pki(
    cert: UploadFile = File(...),
    ca: UploadFile | None = File(None),
):
    cert_bytes = await cert.read()
    cert_obj = _load_cert(cert_bytes)

    now = datetime.now(timezone.utc)
    not_before = cert_obj.not_valid_before.replace(tzinfo=timezone.utc)
    not_after = cert_obj.not_valid_after.replace(tzinfo=timezone.utc)

    valid_by_date = not_before <= now <= not_after

    result = {
        "ok": valid_by_date,
        "valid_by_date": valid_by_date,
        "subject": cert_obj.subject.rfc4514_string(),
        "issuer": cert_obj.issuer.rfc4514_string(),
        "serial_number": str(cert_obj.serial_number),
        "not_before": not_before.isoformat(),
        "not_after": not_after.isoformat(),
    }

    if ca is not None:
        ca_bytes = await ca.read()
        ca_obj = _load_cert(ca_bytes)
        result["ca_subject"] = ca_obj.subject.rfc4514_string()
        result["issuer_matches_ca_subject"] = (cert_obj.issuer == ca_obj.subject)

    return result
