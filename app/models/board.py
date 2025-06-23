from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Board(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    owner: Mapped[str]
    cards: Mapped[list["Card"]] = relationship(back_populates="board")

    def to_dict(self):
        board_as_dict = {}
        board_as_dict["id"] = self.id
        board_as_dict["title"] = self.title
        board_as_dict["owner"] = self.owner

        if self.cards:
            board_as_dict["cards"] = [card.to_dict() for card in self.cards]
        else:
            board_as_dict["cards"] = []

        return board_as_dict

    @classmethod
    def from_dict(cls, board_data):
        return cls(title=board_data["title"], owner=board_data["owner"])