from domain.certificate import Certificate
from domain.certificate_repository import CertificateRepository
from infrastructure.storage_adapter import StorageAdapter

class CertificateService:
    def __init__(self, repository: CertificateRepository, storage: StorageAdapter):
        self.repository = repository
        self.storage = storage

    def process_certificate(self, file: bytes, filename: str, password: str) -> Certificate:
        # Guardar en Storage
        p12_storage_url = self.storage.upload_file(filename, file)

        # Simular conversión de P12 a PEM
        private_key_filename = filename.replace(".p12", "_private.pem")
        public_cert_filename = filename.replace(".p12", "_public.pem")

        private_key_url = self.storage.upload_file(private_key_filename, b"PRIVATE KEY DUMMY")
        public_cert_url = self.storage.upload_file(public_cert_filename, b"PUBLIC CERT DUMMY")

        # Guardar en la base de datos
        certificate = Certificate(
            id=None,  # Será asignado por la BD
            name=filename,
            storage_url=p12_storage_url,
            private_key_url=private_key_url,
            public_cert_url=public_cert_url
        )

        return self.repository.save(certificate)
