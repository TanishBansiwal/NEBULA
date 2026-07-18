from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    filename: str
    filetype: str
    filesize: int
    created_at: datetime

    class Config:
        from_attributes = True