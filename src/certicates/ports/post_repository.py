from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi import UploadFile
from io import BytesIO
from src.certificates.application.certificate_service import convert_p12_to_pom
from src.certificates.domain.certificate_model import CertificateModel


@app.post("/convert_certificate/")
async def convert_certificate(certificate: CertificateModel):
    try:
        # Leer el archivo cargado
        file = certificate.file
        password = certificate.password

        # Convierte el archivo .p12 a .pom
        pom_bytes = convert_p12_to_pom(BytesIO(await file.read()), password)

        # Retornar el archivo .pom convertido
        return {
            "filename": f"{certificate.config_id}.pom",
            "file": pom_bytes.getvalue()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")