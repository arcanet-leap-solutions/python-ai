from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..domain.certificate_model import CertificateModel


class Certificate(BaseModel):
    name: str
    private_key: str
    public_cert: str


class CertificateRepository:
    @staticmethod
    def save_certificate(db: Session, name: str, storage_url: str, private_key_url: str, public_cert_url: str):
        certificate = CertificateModel(
            name=name,
            storage_url=storage_url,
            private_key_url=private_key_url,
            public_cert_url=public_cert_url
        )
        db.add(certificate)
        db.commit()
        db.refresh(certificate)  # Para obtener el ID generado
        return {
            "id": certificate.id,
            "storage_url": certificate.storage_url,
            "private_key_url": certificate.private_key_url,
            "public_cert_url": certificate.public_cert_url
        }
        