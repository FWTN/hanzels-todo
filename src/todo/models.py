from dataclasses import dataclass
from datetime import datetime
from datetime import datetime
from uuid import UUID


@dataclass
class Todo():
    id: UUID | None
    text: str
    create_time: datetime
    status: int
    resolve_time: datetime | None

    def __eq__(self, other) -> bool:
        return self.id == other.id