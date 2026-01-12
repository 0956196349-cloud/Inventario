from datetime import datetime, timezone
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def load_cert_from_pem(pem_str: str) -> x509.Certificate:
    data = pem_str.encode("utf-8")
    return x509.load_pem_x509_certificate(data, default_backend())

def basic_cert_checks(cert: x509.Certificate) -> dict:
    now = datetime.now(timezone.utc)

    not_before = cert.not_valid_before.replace(tzinfo=timezone.utc)
    not_after = cert.not_valid_after.replace(tzinfo=timezone.utc)

    if now < not_before:
        return {"ok": False, "reason": "Certificado aún no es válido (notBefore)."}
    if now > not_after:
        return {"ok": False, "reason": "Certificado expirado (notAfter)."}

    return {"ok": True}

def cert_summary(cert: x509.Certificate) -> dict:
    return {
        "subject": cert.subject.rfc4514_string(),
        "issuer": cert.issuer.rfc4514_string(),
        "serial_number": str(cert.serial_number),
        "not_before": cert.not_valid_before.isoformat(),
        "not_after": cert.not_valid_after.isoformat(),
    }
