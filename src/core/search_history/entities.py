from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class SearchHistoryItemDTO:
    id: UUID
    query: str
    created_at: datetime
