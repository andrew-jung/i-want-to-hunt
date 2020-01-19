import json

import fire

"""
Data object from mhw-db:
{
    "id": 2,
    "name": "Jagras",
    "type": "small",
    "species": "fanged wyvern",
    "description": "Members of the Great Jagras pack, these smaller monsters will flee upon seeing one of their own perish. They're also known for ambushing larger monsters at a moment's notice.",
    "elements": [],
    "ailments": [],
    "locations": [{ "id": 1, "name": "Ancient Forest", "zoneCount": 17 }],
    "resistances": [],
    "weaknesses": [
        { "element": "fire", "stars": 1, "condition": null },
        { "element": "thunder", "stars": 1, "condition": null }
    ],
    "rewards": []
}

API expected POST request:

{
    "name": "Bob",
    "description": "Big idiot",
    "species": "flying wyvern",
	"elements": ["fire"],
    "weaknesses": [
    	{
    		"element": "fire",
    		"stars": 1,
    		"condition": "covered in gas"
    	}
    ],
    "resistances": [
    	{
    		"element": "ice",
            "condition": none
    	}
    ],
    "images": [
    	{
    		"name": "big bad monster",
    		"url": "https://www.google.com"
    	}
    ],
    "ailments": [
    	{
    		"name": "Blastblight",
    		"actions": [
    			"roll", "nullberry"
    		]
    	}
    ],
    "size": "large"
}

"""


class MonsterMigrator:
    IGNORED_KEYS = ["id", "locations", "rewards"]
    API_URL = "localhost:8000/monsters"  # TODO: env?

    def create_monsters_from_file(self, filename=None):
        if not filename:
            raise Exception("Pass a valid json file")
        with open(filename) as json_file:
            data = json.load(json_file)

        cleaned_monster_list = self._clean_monster_json_list(data)
        # Call to our beloved API to create them:
        for monster_dict in cleaned_monster_list:
            self.call_api(monster_dict)

    async def call_api(self, data):
        async with httpx.AsyncClient() as client:
            await client.post(self.API_URL, data=monster_dict)

    def _clean_monster_json_list(self, monsters):
        cleaned_list = []

        for monster in monsters:
            for attribute, value in monster.copy().items():
                if attribute in self.IGNORED_KEYS:
                    monster.pop(attribute, None)
            cleaned_list.append(monster)
        return cleaned_list

    # TODO: Add other CLI helpers, then extract CLI things somewhere else.


if __name__ == "__main__":
    fire.Fire(MonsterMigrator)
