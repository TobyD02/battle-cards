import random
from typing import Sequence, Dict, Any, Union

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select, func

from src.entity.card_base_model import CardBaseModel
from src.entity.card_model import CardModel
from src.entity.card_variant_model import CardVariantModel


class CardBaseRepository:
    def __init__(self, sqlite_root_dir: str):
        self.sqlite_root_dir = sqlite_root_dir
        self.engine = create_engine("sqlite:///" + sqlite_root_dir)
        SQLModel.metadata.create_all(self.engine)

    def insert_card(self, base_card: CardBaseModel) -> int:
        with Session(self.engine) as session:
            session.add(base_card)
            session.commit()
            session.refresh(base_card)

            # Create the 4 variants
            for holo, negative, gold in [
                (False, False, False),
                (False, False, True),
                (False, True, False),
                (False, True, True),
                (True,  False, False),
                (True,  False, True),
                (True,  True, False),
                (True,  True, True),
            ]:
                card = CardVariantModel(
                    base_card_id=base_card.id,        # all card columns flattened
                    negative=negative,
                    gold=gold,
                    holo=holo
                )
                session.add(card)
                session.flush()  # assigns the ID without committing

            session.commit()
            return base_card.id

    def get_base_card_id_by_label(self, card_label: str) -> Union[int, None]:
        with Session(self.engine) as session:
            statement = select(CardBaseModel).where(CardBaseModel.label==card_label)
            result = session.exec(statement).one_or_none()
            if result is None:
                return None
            return result.id

    def get_all_cards(self) -> Sequence[CardBaseModel]:
        with Session(self.engine) as session:
            query=(select(CardVariantModel, CardBaseModel)
                .join(CardBaseModel, CardBaseModel.id == CardVariantModel.base_card_id))

            result=session.exec(query).all()

            cards = []
            for variant, base in result:
                cards.append(self._build_card_from_variant_and_base(variant, base))
            return cards

    def get_card_variant(self, base_card_id: int, negative: bool, gold: bool, holo: bool) -> CardModel:
        with Session(self.engine) as session:
            query = (
                select(CardVariantModel, CardBaseModel)
                .join(CardBaseModel, CardBaseModel.id == CardVariantModel.base_card_id)
                .where(
                    CardVariantModel.base_card_id == base_card_id,
                    CardVariantModel.negative == negative,
                    CardVariantModel.gold == gold,
                    CardVariantModel.holo == holo,
                    )
            )

            result = session.exec(query).one_or_none()
            if not result:
                return None

            variant, base = result
            return self._build_card_from_variant_and_base(variant, base)

    def get_all_card_variants(self, base_card_id: int) -> Sequence[CardModel]:
        with Session(self.engine) as session:
            query=(select(CardVariantModel, CardBaseModel)
                   .join(CardBaseModel, CardBaseModel.id == CardVariantModel.base_card_id)
                   .where(CardVariantModel.base_card_id == base_card_id))

            result=session.exec(query).all()
            cards = []
            for variant, base in result:
                cards.append(self._build_card_from_variant_and_base(variant, base))
            return cards

    def get_random_base_card_id(self):
        with Session(self.engine) as session:
            query = (
                select(CardBaseModel.id)
                .order_by(func.random())
                .limit(1)
            )
            return session.exec(query).one()

    def _build_card_from_variant_and_base(self, variant: CardVariantModel, base: CardBaseModel) -> CardModel:
        return CardModel(
            id=variant.id,
            base_card_id=base.id,
            label=base.label,
            name=base.name,
            strength=base.strength,
            dexterity=base.dexterity,
            wisdom=base.wisdom,
            intelligence=base.intelligence,
            charisma=base.charisma,
            constitution=base.constitution,
            description=base.description,
            image_url=base.image_url,
            holo=variant.holo,
            negative=variant.negative,
            gold=variant.gold,
        )