import json

import fire
import httpx


class MonsterMigrator:
    IGNORED_KEYS = ["id", "locations", "rewards"]
    API_URL = "http://localhost:8000/monsters"  # TODO: env?

    def create_monsters_from_file(self, filename=None):
        if not filename:
            raise Exception("Pass a valid json file")
        with open(filename) as json_file:
            data = json.load(json_file)

        cleaned_monster_list = self._clean_monster_json_list(data)

        # Call to our beloved API to create them:
        for monster_dict in cleaned_monster_list:
            self._call_api(monster_dict)

    def _call_api(self, data):
        data = json.dumps(data)
        print(data)
        httpx.post(self.API_URL, data=data)

    def _clean_monster_json_list(self, monsters):
        cleaned_list = []

        for monster in monsters:
            for attribute, value in monster.copy().items():
                if attribute in self.IGNORED_KEYS:
                    monster.pop(attribute, None)
                if attribute == "type":
                    monster["size"] = monster.pop(attribute, None)
                if attribute == "ailments":
                    for i, ailment in enumerate(value):
                        ailment = self._deconstruct_ailment(ailment)
                        if ailment:
                            monster[attribute][i] = ailment
            cleaned_list.append(monster)

        return cleaned_list

    def _deconstruct_ailment(self, ailment):
        """
        If there is an ailment, we only care abouts its name and recovery actions
        """
        formatted_ailment = {
            "name": ailment.get("name"),
            "actions": ailment.get("recovery", {}).get("actions", []),
        }
        return formatted_ailment


if __name__ == "__main__":
    fire.Fire(MonsterMigrator)
