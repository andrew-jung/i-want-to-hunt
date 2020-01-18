import json
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


@app.get("/monsters/")
async def get_all_monsters(name: str = None):
    """
    Route for returning monsters:
        - By default, return all monsters
        - Query params: ?name= Monster name to search and return a single Monster
                        ?names= List of monster names to return a list of monsters, will take precendence over 'name' param
    """
    query = monsters_db.select()
    if name:
        # Search for the Monster in the DB:
        monster = Monster(
            name=name,
            description="Test description",
            species="Dragon",
            weaknesses=[Weakness(element="fire", stars=1)],
            resistances=[Resistance(element="water")],
        )
        monster_repr = monster.json()
        return json.loads(monster_repr)

    return await database.fetch_all(query)


@app.post("/monsters/", response_model=Monster)
async def create_monster(monster: Monster):
    query = monsters_db.insert().values(
        name=monster.name,
        description=monster.description,
        species=monster.species,
        size=monster.size,
        weaknesses=[
            Weakness(
                element=weakness.element,
                stars=weakness.stars,
                condition=getattr(weakness, "condition", ""),
            )
            for weakness in monster.weaknesses
        ],
        resistances=[
            Resistance(
                element=resistance.element,
                condition=getattr(resistance, "condition", ""),
            )
            for resistance in monster.resistances
        ],
        images=[Image(name=image.name, url=image.url) for image in monster.images],
        ailments=[
            Ailment(name=ailment.name, actions=ailment.actions)
            for ailment in monster.ailments
        ],
    )

    last_record_id = await database.execute(query)
    return {**monster.dict(), "id": last_record_id}
