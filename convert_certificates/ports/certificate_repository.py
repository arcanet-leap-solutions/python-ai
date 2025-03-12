from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..domain.certificate_model import CertificateModel


class Certificate(BaseModel):
    name: str
    private_key: str
    public_cert: str


class CertificateRepository:
    @staticmethod
    def save_certificate(db: Session, name: str, private_key: str, public_cert: str):
        certificate = CertificateModel(name=name, private_key=private_key, public_cert=public_cert)
        db.add(certificate)
        db.commit()
        db.refresh(certificate)  # Esto actualiza el objeto con el ID generado por la BD
        return {"id": certificate.id, "private_key": certificate.private_key}

