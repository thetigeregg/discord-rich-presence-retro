from typing import Optional
import re
import unidecode
from config.constants import platform_clean_names, modern_platforms, region_labels
import time


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
    if platform in platform_clean_names:
        return platform_clean_names[platform]
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


# def set_discord_presence(game_data):
#     client_id = get_client_id(
#         game_data["platform"]
#     )  # Replace with your app's client ID
#     RPC = Presence(client_id)
#     RPC.connect()

#     start_time = int(time.time())
#     platform_display = get_final_platform(game_data["platform"])
#     region_display = split_and_check(game_data["labels"], region_labels)
#     if region_display:
#         region_display = ", " + region_display
#     year = get_year(game_data["release_date"])
#     state_display = (
#         platform_display + " (" + (year or "") + (region_display or "") + ")"
#     )

#     large_key = sanitize_game_name(game_data["name"] + "_" + game_data["platform"])
#     print(large_key)
