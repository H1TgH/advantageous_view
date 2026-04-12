from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SearchHistoryItemSchema(BaseModel):
    id: UUID
    query: str
    created_at: datetime
