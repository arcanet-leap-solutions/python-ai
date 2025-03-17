from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional

class CertificateModel(BaseModel):
    config_id: int
    file: UploadFile
    password: str
