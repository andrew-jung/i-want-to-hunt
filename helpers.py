"""
SQLite can't handle lists/arrays, convert a list to a string for SQLite.

We use Lists for: Ailments, Weaknesses, Resistances, Images.

We can write tuple strings delimited by whatever to separate them.

"""


def _convert_ailments_to_string(self, ailments):
    return


def _convert_weaknesses_to_string(self, weaknesses):
    # Weakness(element, stars, conditions[nullable])
    return


def _convert_resistances_to_string(self, resistances):
    return


def _convert_images_to_string(self, images):
    return


def _convert_strings_to_list(self, string):
    # Reading from SQLite, we should make it pretty for the API.
    return
