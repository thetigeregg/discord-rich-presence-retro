from fuzzywuzzy import process
from prompt_toolkit.completion import Completer, Completion


class GameNameCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.text_before_cursor.lower()
        suggestions = process.extract(
            word, get_game_name_suggestions(self.games_dict), limit=10
        )
        for suggestion, score in suggestions:
            if score > 70:  # adjust the score as needed
                yield Completion(suggestion, start_position=-len(word))

    def __init__(self, games_dict):
        self.games_dict = games_dict


def get_game_name_suggestions(games_dict):
    return list(games_dict.keys())
