from fuzzywuzzy import process
from prompt_toolkit.completion import Completer, Completion


class GameNameCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.text_before_cursor.lower()
        game_name_suggestions = get_game_name_suggestions(self.games_dict)
        suggestions = process.extract(
            word, [game[0] for game in game_name_suggestions], limit=10
        )
        for suggestion, score in suggestions:
            if score > 70:  # adjust the score as needed
                for game_name, game_name_with_platform in game_name_suggestions:
                    if game_name == suggestion:
                        yield Completion(
                            game_name_with_platform, start_position=-len(word)
                        )

    def __init__(self, games_dict):
        self.games_dict = games_dict


def get_game_name_suggestions(games_dict):
    return [
        (game["name"], game["name"] + " (" + game["platform"] + ")")
        for game in games_dict.values()
    ]
