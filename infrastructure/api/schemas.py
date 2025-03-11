from pydantic import BaseModel
from typing import Optional

class P12ProcessRequest(BaseModel):
    config_id: str
    file_name: Optional[str] = None

class ProcessResponse(BaseModel):
    success: bool
    message: str