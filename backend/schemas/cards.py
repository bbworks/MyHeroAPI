from enum import Enum
from typing import Annotated, Optional, Literal, Union
from pydantic import BaseModel, Field, HttpUrl


class Zone(str, Enum):
    high = "High"
    low = "Low"
    mid = "Mid"

class Symbol(str, Enum):
    air = "Air"
    all = "All"
    chaos = "Chaos"
    death = "Death"
    earth = "Earth"
    evil = "Evil"
    fire = "Fire"
    good = "Good"
    infinity = "Infinity"
    life = "Life"
    order = "Order"
    void = "Void"
    water = "Water"


class Set(str, Enum):
    s1 = "My Hero Academia"
    s2 = "Crimson Rampage"
    special = "Provisional Showdown"

class CharacterCard(BaseModel):
    max_health: int
    starting_hand_size: int
    type: Literal['Character']


class AttackCard(BaseModel):
    ability: str | None
    attack_keywords: list[str]
    attack_zone: Zone
    damage: int
    speed: int
    type: Literal['Attack']

class FoundationCard(BaseModel):
    type: Literal['Foundation']

class ActionCard(BaseModel):
    type: Literal['Action']

class AssetCard(BaseModel):
    type: Literal['Asset']


class AllCards(BaseModel):

    id: int
    name: str
    url: str

class Card(BaseModel):
    block_modifier: int
    block_zone: str
    check: int
    description: list[str | list[str]] | None = None
    id: int
    image_url: HttpUrl | None = None
    keyword: list[str] | None = None
    name: str
    play_difficulty: int
    rarity: str
    set: Set
    symbols: list[Symbol]
    type_attributes: Annotated[Union[CharacterCard, AttackCard, AssetCard, ActionCard, FoundationCard], Field(discriminator='type')] | None = None

    class Config:
        case_sensitive = False
        orm_mode = True


class UpdateCard(BaseModel):
    block_modifier: Optional[int] = None
    block_zone: Optional[str] = None
    check: Optional[int] = None
    description: Optional[list[str]] = None
    id: Optional[int] = None
    image_url: Optional[HttpUrl]= None
    keyword: Optional[list[str]] = None
    name: Optional[str] = None
    play_difficulty: Optional[int] = None
    rarity: Optional[str] = None
    set: Optional[Set] = None
    symbols: Optional[list[Symbol]] = None
    type_attributes: Optional[Annotated[Union[CharacterCard, AttackCard, AssetCard, ActionCard, FoundationCard], Field(discriminator='type')]] = None

    class Config:
        orm_mode = True
