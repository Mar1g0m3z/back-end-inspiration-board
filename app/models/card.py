from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[int]
    board_id: Mapped[Optional[int]]=mapped_column(ForeignKey("board.id"))
    board: Mapped[Optional["Board"]] = relationship(back_populates="cards")

    def to_dict(self):
        card_as_dict = {}

        card_as_dict["id"] = self.id
        card_as_dict["message"] = self.message
        card_as_dict["likes_count"] = self.likes_count
        card_as_dict["board_id"] = self.board_id

        return card_as_dict

    @classmethod
    def from_dict(cls, card_data):
        likes_count = 0
        return cls(message=card_data["message"],
                   likes_count=likes_count,
                   board_id=card_data["board_id"])