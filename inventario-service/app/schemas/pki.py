from pydantic import BaseModel, Field

class PkiVerifyIn(BaseModel):
    pem_cert: str = Field(min_length=20)

class PkiVerifyOut(BaseModel):
    ok: bool
    subject: str | None = None
    issuer: str | None = None
    serial_number: str | None = None
    not_before: str | None = None
    not_after: str | None = None
    message: str
