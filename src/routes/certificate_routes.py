from fastapi import APIRouter, UploadFile, File, Form,Depends
from ..application.certificate_service import CertificateService
from sqlalchemy.orm import Session
from ..config.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/convert/")
async def convert_certificate(
    file: UploadFile = File(...),
    password: str = Form(...)
):
    file_content = await file.read()
    result = CertificateService.process_certificate(file_content, file.filename, password)

    if result is None:
        return {"error": "No se pudo procesar el certificado"}

    return {
        "message": "Certificate processed successfully",
        "id": result["id"],
        "storage_url": result["storage_url"],
        "private_key_url": result["private_key_url"],
        "public_cert_url": result["public_cert_url"]
    }