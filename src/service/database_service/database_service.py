import random
from typing import Sequence

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select, func

from src.entity.card_model import CardModel


class DatabaseService:
    def __init__(self, sqlite_root_dir: str):
        self.sqlite_root_dir = sqlite_root_dir
        self.engine = create_engine("sqlite:///" + sqlite_root_dir)
        SQLModel.metadata.create_all(self.engine)

    def insert_card(self, card: CardModel) -> CardModel:
        with Session(self.engine) as session:
            session.add(card)
            session.commit()
            session.refresh(card)
            return card

    def get_card_by_label(self, card_label: str) -> CardModel:
        with Session(self.engine) as session:
            statement = select(CardModel).where(CardModel.label==card_label)
            return session.exec(statement).one()

    def get_all_cards(self) -> Sequence[CardModel]:
        with Session(self.engine) as session:
            statement = select(CardModel)
            return session.exec(statement).all()


    def get_all_cards_count(self) -> int:
        with Session(self.engine) as session:
            statement = select(func.count()).select_from(CardModel)
            return session.exec(statement).one()


    def get_random_card(self) -> CardModel | None:
        with Session(self.engine) as session:
            # get max id
            max_id = session.exec(select(func.max(CardModel.id))).one()

            if max_id is None:
                return None  # no rows yet

            random_id = random.randint(1, max_id)
            card = session.get(CardModel, random_id)
            return card