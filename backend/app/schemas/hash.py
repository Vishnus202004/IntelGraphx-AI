from datetime import datetime
from pydantic import BaseModel, ConfigDict


class HashBase(BaseModel):
    competitor_id: int
    url: str
    content_hash: str


class HashCreate(HashBase):
    pass


class HashUpdate(BaseModel):
    content_hash: str


class HashInDBBase(HashBase):
    id: int
    checked_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Hash(HashInDBBase):
    pass
