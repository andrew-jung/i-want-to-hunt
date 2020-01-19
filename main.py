import ast
from typing import List

import sqlalchemy
from databases import Database
from fastapi import FastAPI

from models import Ailment, Image, Monster, Resistance, Weakness

"""
SQLite config, can remove later, but this is for instant-setup for anyone.
"""

DATABASE_URL = "sqlite:///./monsters.db"
database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
monsters_db = sqlalchemy.Table(
    "monsters",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("species", sqlalchemy.String),
    sqlalchemy.Column("elements", sqlalchemy.String),
    sqlalchemy.Column("weaknesses", sqlalchemy.String),
    sqlalchemy.Column("resistances", sqlalchemy.String),
    sqlalchemy.Column("ailments", sqlalchemy.String),
    sqlalchemy.Column("images", sqlalchemy.String),
    sqlalchemy.Column("size", sqlalchemy.String),
)
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def read_root():
    return "Nothing to see here..."


CONVERT_KEYS = ["ailments", "elements", "images", "resistances", "weaknesses"]


def _to_representation(monster):
    monster_dict = dict(monster)
    for attribute, value in monster_dict.copy().items():
        if attribute in CONVERT_KEYS:
            value = ast.literal_eval(value)
            monster_dict[attribute] = value
    return monster_dict


@app.get("/monsters/")
async def get_all_monsters(name: str = None):
    """
    Endpoint for returning monsters:
        - Default: return all monsters
        - Query param (name): Monster name to search and return a single Monster
    """
    query = monsters_db.select()
    if name:
        query = query.where(monsters_db.columns.name == name)
        # TODO: Add a like filter, right now it's case-sensitive.
    results = await database.fetch_all(query)
    for idx, monster in enumerate(results):
        monster = _to_representation(monster)
        results[idx] = monster
    return {"monsters": results}


@app.post("/monsters/", response_model=Monster)
async def create_monster(*, monster: Monster):
    """
    Endpoint to handle Monster creation
    """
    query = None

    weaknesses = str(
        [
            Weakness(
                element=weakness.element,
                stars=weakness.stars,
                condition=getattr(weakness, "condition", ""),
            ).dict()
            for weakness in monster.weaknesses
            if monster.weaknesses
        ]
    )
    resistances = str(
        [
            Resistance(
                element=resistance.element,
                condition=getattr(resistance, "condition", ""),
            ).dict()
            for resistance in monster.resistances
            if monster.resistances
        ]
    )
    images = str(
        [
            Image(name=image.name, url=image.url).dict()
            for image in monster.images
            if monster.images
        ]
    )
    ailments = str(
        [
            Ailment(name=ailment.name, actions=ailment.actions).dict()
            for ailment in monster.ailments
            if monster.ailments
        ]
    )
    elements = str([element for element in monster.elements if monster.elements])
    query = monsters_db.insert().values(
        name=monster.name,
        description=monster.description,
        species=monster.species,
        size=monster.size.name,
        weaknesses=weaknesses,
        resistances=resistances,
        images=images,
        ailments=ailments,
        elements=elements,
    )

    last_record_id = await database.execute(query)
    return {**monster.dict(), "id": last_record_id}


# TODO: PUT/PATCH + DELETE
