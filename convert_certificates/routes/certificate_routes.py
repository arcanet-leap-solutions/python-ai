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
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    file_content = await file.read()
    result = CertificateService.process_certificate(file_content, file.filename, password)
    return {"message": "Certificate processed successfully", "id": result["id"], "private_key": result["private_key"]}
