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

    return {"all_monsters": []}


"""
Need to protect this later so garbage isn't pushed to the db.
Alternatively, we can have two databases, one that is read for the page, and another that is called 'updates.db',
We can manually (cry) review entries in updates, and push them to monsters.db
Or we can have pure chaos.
"""


@app.post("/monsters/", response_model=Monster)
async def create_monster(monster: Monster):
    # First try to construct models from Monster values:

    # What does a POST request look like even?:
    """
    {
        "name": "Diablos",
        "description": "Big idiot",
        "species": "flying wyvern",
        "weaknesses": [{"element": "fire", "stars": 1, "conditions": "covered in gas"}],
        "resistances": [{"element": "ice"}],
        "images": [{"name": "big bad monster", "url": "google.com"}],
        "ailments": [{"name": "Blastblight", "actions": ["nullbery", "dodge"]}]
    }
    """
    # query = monsters_db.insert().values(
    #     name=monster.name,
    #     description=monster.description,
    #     species=monster.species,
    #     weaknesses=[
    #         Weakness(element=monster_weakness.element, stars=monster_weakness.stars) for monster_weakness in monster.weaknesses
    #     ],
    #     resistances=[Resistance(element="water")],
    #     images=[Image()]
    #     ailments=[Ailment()]
    # )
    # last_record_id = await database.execute(query)
    # return {**monster.dict(), "id": last_record_id}
