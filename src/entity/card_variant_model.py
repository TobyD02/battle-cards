from sqlmodel import SQLModel, Field
from src.entity.card_base_model import CardBaseModel

class CardVariantModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    base_card_id: int = Field(default=None, foreign_key="cardbasemodel.id")
    holo: bool
    negative: bool
    gold: bool