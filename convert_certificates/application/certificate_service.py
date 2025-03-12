from ..adapters.openssl_adapter import OpenSSLAdapter
from ..adapters.storage_adapter import StorageAdapter
from ..ports.certificate_repository import CertificateRepository
from ..config.db import SessionLocal
import tempfile
import os

from sqlalchemy.exc import SQLAlchemyError

class CertificateService:
    @staticmethod
    def process_certificate(file: bytes, filename: str, password: str):
        try:
            # Guardar en Storage
            p12_storage_url = StorageAdapter.upload_file(filename, file)

            # Convertir .p12 a .pem
            private_key_filename = filename.replace(".p12", "_private.pem")
            public_cert_filename = filename.replace(".p12", "_public.pem")

            private_key_url = StorageAdapter.upload_file(private_key_filename, b"PRIVATE KEY DUMMY")
            public_cert_url = StorageAdapter.upload_file(public_cert_filename, b"PUBLIC CERT DUMMY")

            # Guardar en la base de datos
            db = SessionLocal()
            result = CertificateRepository.save_certificate(db, filename, p12_storage_url, private_key_url, public_cert_url)
            db.close()

            if not result:
                raise ValueError("No se pudo guardar en la base de datos")

            return result
        except SQLAlchemyError as e:
            print(f"Error en la base de datos: {str(e)}")
            return None
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return None