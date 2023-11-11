import csv

from utils.text import normalize_game_name
from config.constants import CONFIG_FILE_PATH


def load_games_list():
    games_dict = {}
    with open(CONFIG_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i >= 5:
                break
            normalized_name = normalize_game_name(row["name"])
            games_dict[normalized_name] = row
    return games_dict
