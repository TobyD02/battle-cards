from pydantic import BaseModel, Field


class CardInfoModel(BaseModel):
    name: str
    strength: int
    dexterity: int
    wisdom: int
    intelligence: int
    charisma: int

    description: str

def generate_card_prompt(context: str, name: str) -> str:
    return f"""
    <context>
    {context}
    </context>
    Generate statistics and information for a card game for the character. Keep the description as a short single sentence bio (less than 255 characters). Base these stats off accurate popculture information, they should reflect the character as accurately as possible. The stats should be between 1 and 100, where 100 is omnipotent/godtier, and 1 is negligable: {name}
    """