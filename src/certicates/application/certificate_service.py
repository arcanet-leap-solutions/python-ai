
from fastapi import HTTPException
from src.certificates.domain.certificate_model import ConvertCertificateModel
from src.certificates.application.certificate_service import convert_p12_to_pom
from io import BytesIO


class PostRepositoryConvertCertificate(ConvertCertificateModel):
    def __init__(self, certificate: ConvertCertificateModel):
        self.certificate = certificate

    def convert_certificate(self):
        try:
            # Leer el archivo cargado
            file = self.certificate.file
            password = self.certificate.password

            # Convierte el archivo .p12 a .pom
            pom_bytes = convert_p12_to_pom(BytesIO(file), password)

            # Retornar el archivo .pom convertido
            return {
                "filename": f"{self.certificate.config_id}.pom",
                "file": pom_bytes.getvalue()
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
        return None