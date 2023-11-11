from typing import Optional
import re
import unidecode
from config.constants import PLATFORM_CLEAN_NAMES


def formatSeconds(seconds: int | float, joiner: Optional[str] = None) -> str:
    seconds = round(seconds)
    timeValues = {"h": seconds // 3600, "m": seconds // 60 % 60, "s": seconds % 60}
    if not joiner:
        return "".join(str(v) + k for k, v in timeValues.items() if v > 0)
    if timeValues["h"] == 0:
        del timeValues["h"]
    return joiner.join(str(v).rjust(2, "0") for v in timeValues.values())


def sanitize_game_name(game_name):
    sanitized = re.sub(r"\W+", "_", game_name).lower()
    return sanitized


def normalize_game_name(name):
    return unidecode.unidecode(name.lower())


def get_final_platform(platform):
    if platform in PLATFORM_CLEAN_NAMES:
        return PLATFORM_CLEAN_NAMES[platform]
    else:
        return platform


def split_and_check(input_string, check_list):
    # Split the input string into a list of trimmed strings
    split_list = [s.strip() for s in input_string.split(",")]

    # Check which elements of split_list are in check_list
    in_list = [s for s in split_list if s in check_list]

    get_first_element(in_list)


def get_first_element(list):
    if list:
        return list[0]
    else:
        return None


def get_year(date_string):
    return date_string.split("-")[0]
