import csv


def load_games_list():
    games_dict = {}
    with open(get_value_from_config_file("csvPath"), "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i >= 5:
                break
            normalized_name = normalize_game_name(row["name"])
            games_dict[normalized_name] = row
    return games_dict
