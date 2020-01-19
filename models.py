from enum import Enum
from typing import List, Optional, Set

from pydantic import BaseModel


class Size(str, Enum):
    small = "small"
    large = "large"


class Image(BaseModel):
    """
    Image path for a Monster
    """

    name: str
    url: str


class Ailment(BaseModel):
    """
    Ailment caused by a Monster and returns a set of actions to resolve it (if applicable.)

    Examples: Blastblight
    """

    name: str
    actions: List[Optional[str]] = None


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
    elements: Set[str] = None
    weaknesses: List[Weakness] = None
    resistances: List[Resistance] = None
    ailments: List[Ailment] = None
    images: List[Image] = [
        Image(name="placeholder", url="https://placekitten.com/200/300")
    ]


class Monsters(BaseModel):
    """
    List of Monsters
    """

    monsters: List[Monster] = None
