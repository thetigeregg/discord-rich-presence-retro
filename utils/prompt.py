from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion


class GameNameCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.text_before_cursor.lower()
        for game_name in get_game_name_suggestions():
            if word in game_name:
                yield Completion(game_name, start_position=-len(word))


def get_game_name_suggestions():
    games_dict = load_games_list()
    return list(games_dict.keys())
