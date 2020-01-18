from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class Size(str, Enum):
    small = "small"
    large = "large"


class Image(BaseModel):
    """
    Image path for a Monster
    """

    name: str
    url: HttpUrl


class Action(BaseModel):
    """
    Model for an Action to resolve an Ailment

    Examples: Dodge/roll, use nullbery, etc.
    """

    action: str


class Ailment(BaseModel):
    """
    Ailment caused by a Monster and returns a list of actions to resolve it (if applicable.)

    Examples: Blastblight
    """

    name: str
    actions: List[Action]


class Resistance(BaseModel):
    """
    Monster's resistance to your weapons/elements, may have a condition before triggered.
    """

    element: str
    condition: Optional[str] = None


class Weakness(BaseModel):
    """
    Monster's weakness and conditions when the weaknesses are available.
    """

    element: str
    stars: int
    condition: Optional[str] = None


class Monster(BaseModel):
    """
    Monster model representation, accumulation of other model/fields.
    """

    name: str
    description: str
    species: str
    size: Size
    elements: List[str] = []
    weaknesses: List[Weakness] = []
    resistances: List[Resistance] = []
    ailments: List[Ailment] = []
    images: List[Image] = []


class Monsters(BaseModel):
    """
    List of Monsters
    """

    monsters: List[Monster] = []
