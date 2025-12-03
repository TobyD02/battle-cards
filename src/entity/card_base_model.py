from sqlmodel import SQLModel, Field

class CardBaseModel(SQLModel, table=True):
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
    image_url: str
    wiki_url: str
