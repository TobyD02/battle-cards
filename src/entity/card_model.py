from sqlmodel import SQLModel, Field

class CardModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    label: str
    name: str
    strength: int
    dexterity: int
    wisdom: int
    intelligence: int
    charisma: int
    constitution: int
    description: str
    aggregate_stats: int
    image_url: str
    wiki_url: str
    holo: bool
