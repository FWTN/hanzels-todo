from dataclasses import dataclass
from datetime import datetime
from datetime import datetime
from typing import Any
from uuid import UUID, uuid1


@dataclass
class Todo():
    id: UUID | None
    text: str
    create_time: datetime
    status: int
    resolve_time: datetime | None

    def __eq__(self, other) -> bool:
        return self.id == other.id

    @staticmethod
    def from_json(json: Any) -> "Todo":
        return Todo(id=UUID(json["id"]),
             text=json["text"],
             create_time=json["create_time"],
             status=json["status"],
             resolve_time=json["resolve_time"]
             )

    @staticmethod
    def from_text(text: str):
        return Todo(id=uuid1(),
             text=text,
             create_time=datetime.now(),
             status=0,
             resolve_time=None)