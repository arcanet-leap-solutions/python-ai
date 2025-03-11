from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FileRecord(BaseModel):
    id: str
    file_name: str
    config_id: str
    pom_content: str
    created_at: datetime = datetime.now()