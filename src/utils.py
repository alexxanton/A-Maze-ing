from random import shuffle


def generate_name(name_seed: str) -> str:
    chars = list(name_seed)
    shuffle(chars)
    name_seed = "".join(chars)
    last = ""
    name = ""
    start = {"0": "rakh'", "1": "ar'", "2": "set", "3": "kha'", "4": "amon",
             "5": "ra'", "6": "thut", "7": "nekh'", "8": "maat", "9": "sekh'"}

    alt = {"0": "sen", "1": "tek", "2": "rah", "3": "ket", "4": "mon",
                  "5": "khe'", "6": "bak", "7": "ren", "8": "ab'", "9": "neb"}

    middle = {"0": "ukt", "1": "to", "2": "ji", "3": "sa", "4": "yok'",
              "5": "go", "6": "khur", "7": "mat'", "8": "ha", "9": "kit"}

    end = {"0": "esh", "1": "akh", "2": "et", "3": "ut", "4": "eshk",
           "5": "ar", "6": "em", "7": "an", "8": "ir", "9": "oth"}

    for i, ch in enumerate(name_seed):
        if i == 0:
            name += start[ch]
        elif i == len(name_seed) - 1:
            name += end[ch]
        else:
            if ch == last:
                name += alt[ch]
                last = ""
            else:
                name += middle[ch]
            last = ch
    return f"Maze name: {name.capitalize()}"
