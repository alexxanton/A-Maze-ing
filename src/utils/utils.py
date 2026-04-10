from random import shuffle, choice
from mazegen import Direction


def generate_name(name_seed: str) -> str:
    """Generate a random name based on a seed."""
    chars = list(name_seed)
    shuffle(chars)
    name_seed = "".join(chars)
    last = ""
    name = ""
    start = {"0": "rakh'", "1": "ar'", "2": "set", "3": "kha'", "4": "amon",
             "5": "ra'", "6": "thut", "7": "nekh'", "8": "ab'", "9": "sekh'"}

    middle = {"0": "ukt", "1": "to", "2": "qal", "3": "sav", "4": "yok",
              "5": "gor", "6": "khur", "7": "maat", "8": "hav", "9": "kit"}

    alt = {"0": "sen", "1": "tek", "2": "rah", "3": "ket", "4": "mon",
           "5": "khe", "6": "bak", "7": "ren", "8": "al", "9": "neb"}

    end = {"0": "'esh", "1": "akh", "2": "'eth", "3": "qut", "4": "eshk",
           "5": "ark", "6": "qem", "7": "an", "8": "'ir", "9": "'oth"}

    for i, ch in enumerate(name_seed):
        if i == 0:
            options = [start, alt]
            option = choice(options)
            name += option[ch]
        elif i == len(name_seed) - 1:
            name += end[ch]
        elif i < 3:
            if ch == last:
                name += alt[ch]
                last = ""
            else:
                name += middle[ch]
            last = ch
    return name.replace("''", "'").capitalize()


def get_direction(x: int, y: int, nx: int, ny: int) -> Direction:
    """Get the direction between two cells."""
    if x > nx:
        return Direction.WEST
    if x < nx:
        return Direction.EAST
    if y > ny:
        return Direction.NORTH
    if y < ny:
        return Direction.SOUTH
    return Direction.NONE
