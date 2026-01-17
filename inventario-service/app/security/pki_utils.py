from cryptography import x509
from cryptography.hazmat.backends import default_backend

def _safe_str(name) -> str:
    try:
        return name.rfc4514_string()
    except Exception:
        return str(name)

def verify_pem_certificate(pem_cert: str) -> dict:
    pem = pem_cert.strip().encode("utf-8")

    cert = x509.load_pem_x509_certificate(pem, default_backend())

    return {
        "subject": _safe_str(cert.subject),
        "issuer": _safe_str(cert.issuer),
        "serial_number": hex(cert.serial_number),
        "not_before": cert.not_valid_before_utc.isoformat(),
        "not_after": cert.not_valid_after_utc.isoformat(),
    }
