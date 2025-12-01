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
    description: str
    image_url: str
    wiki_url: str
