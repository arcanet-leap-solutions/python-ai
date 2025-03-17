from sqlalchemy.orm import Session
from domain.certificate_repository import CertificateRepository
from domain.certificate import Certificate
from infrastructure.models import CertificateModel

class CertificateRepositoryPG(CertificateRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, certificate: Certificate) -> Certificate:
        cert_model = CertificateModel(
            name=certificate.name,
            storage_url=certificate.storage_url,
            private_key_url=certificate.private_key_url,
            public_cert_url=certificate.public_cert_url
        )
        self.db.add(cert_model)
        self.db.commit()
        self.db.refresh(cert_model)
        certificate.id = cert_model.id
        return certificate

    def get_by_id(self, cert_id: int) -> Certificate:
        cert_model = self.db.query(CertificateModel).filter_by(id=cert_id).first()
        if cert_model:
            return Certificate(
                id=cert_model.id,
                name=cert_model.name,
                storage_url=cert_model.storage_url,
                private_key_url=cert_model.private_key_url,
                public_cert_url=cert_model.public_cert_url
            )
        return None
