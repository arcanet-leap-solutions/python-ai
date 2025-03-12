from ..adapters.openssl_adapter import OpenSSLAdapter
from ..adapters.storage_adapter import StorageAdapter
from ..ports.certificate_repository import CertificateRepository
from ..config.db import SessionLocal

class CertificateService:
    @staticmethod
    def process_certificate(file: bytes, filename: str, password: str):
        p12_path = StorageAdapter.save_file(filename, file)
        pem_path = p12_path.replace(".p12", ".pem")

        OpenSSLAdapter.convert_p12_to_pem(p12_path, pem_path, password)

        with open(pem_path, "r") as pem_file:
            pem_content = pem_file.read()

        private_key = "\n".join([line for line in pem_content.split("\n") if "PRIVATE KEY" in line])
        public_cert = "\n".join([line for line in pem_content.split("\n") if "CERTIFICATE" in line])

        db = SessionLocal()
        result = CertificateRepository.save_certificate(db, filename, private_key, public_cert)
        db.close()

        return result  # Retornamos id y private_key