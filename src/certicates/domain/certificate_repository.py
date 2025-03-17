from abc import ABC, abstractmethod
from typing import List

class CertificateRepository(ABC):
    @abstractmethod
    def convert_to_pem(self, file: str, filename: str, password: str) -> None:
        pass
    
    @abstractmethod
    def get_private_key(self, pem_content: str) -> str:
        pass
    
    @abstractmethod
    def get_public_cert(self, pem_content: str) -> str:
        pass

class ConvertCertificateRepository(ABC):
    @abstractmethod
    def convert_p12_to_pom(p12_file: BytesIO, password: str) -> BytesIO:
        pass