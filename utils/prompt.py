from fuzzywuzzy import process
from prompt_toolkit.completion import Completer, Completion


class GameNameCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.text_before_cursor.lower()
        suggestions = process.extract(word, self.game_names, limit=10)
        for suggestion, score in suggestions:
            if score > 70:  # adjust the score as needed
                display_name = self.game_name_to_display_name[suggestion]
                yield Completion(
                    suggestion, start_position=-len(word), display=display_name
                )

    def __init__(self, games_dict):
        self.game_names = [game["name"] for game in games_dict.values()]
        self.game_name_to_display_name = {
            game["name"]: game["name"] + " (" + game["platform"] + ")"
            for game in games_dict.values()
        }


def get_game_name_suggestions(games_dict):
    return [
        (game["name"], game["name"] + " (" + game["platform"] + ")")
        for game in games_dict.values()
    ]
