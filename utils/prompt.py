from prompt_toolkit.completion import Completer, Completion


class GameNameCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.text_before_cursor.lower()
        for game_name in get_game_name_suggestions(self.games_dict):
            if word in game_name:
                yield Completion(game_name, start_position=-len(word))

    def __init__(self, games_dict):
        self.games_dict = games_dict


def get_game_name_suggestions(games_dict):
    return list(games_dict.keys())
