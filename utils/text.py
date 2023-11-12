from typing import Optional
import re
import unidecode
from config.constants import PLATFORM_CLEAN_NAMES, REGION_LABELS
from utils.logging import logger, formatter


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


def get_final_platform(game_data, region_for_display):
    logger.debug("%s", "Getting final platform")

    logger.debug("%s: '%s'", "Region for display", region_for_display)

    if game_data["platform"] in PLATFORM_CLEAN_NAMES:
        return PLATFORM_CLEAN_NAMES[game_data["platform"]]
    elif game_data["platform"] == "TurboGrafx-16/PC Engine":
        if region_for_display == "JP":
            return "PC Engine"
        else:
            return "TurboGrafx-16"
    elif game_data["platform"] == "Turbografx-16/PC Engine CD":
        if region_for_display == "JP":
            return "PC Engine CD"
        else:
            return "TurboGrafx-CD"
    else:
        return game_data["platform"]


def split_and_check(input_string, check_list):
    # Split the input string into a list of trimmed strings
    split_list = [s.strip() for s in input_string.split(",")]

    logger.debug("%s: '%s'", "Split string into", split_list)

    # Check which elements of split_list are in check_list
    in_list = [s for s in split_list if s in check_list]

    logger.debug("%s: '%s'", "Which element is in the list", in_list)

    return get_first_element(in_list)


def get_final_region(label_string):
    logger.debug("%s: '%s'", "Labels for game", label_string)

    region_label = split_and_check(label_string, REGION_LABELS)

    logger.debug("%s: '%s'", "Region from label", region_label)

    if region_label is not None and region_label != "":
        return region_label


def get_first_element(list):
    if list:
        return list[0]
    else:
        return None


def get_year(date_string):
    return date_string.split("-")[0]
