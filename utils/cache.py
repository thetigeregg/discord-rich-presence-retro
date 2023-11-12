from utils.text import normalize_game_name
from .logging import logger
from config.constants import CACHE_FILE_PATH, RECENTS_FILE_PATH
from typing import Any, Dict
import json
import os
import time
from typing import Any, List

cache: dict[str, Any] = {}


def loadCache() -> None:
    if not os.path.isfile(CACHE_FILE_PATH):
        return
    try:
        with open(CACHE_FILE_PATH, "r", encoding="UTF-8") as cacheFile:
            cache.update(json.load(cacheFile))
    except:
        root, ext = os.path.splitext(CACHE_FILE_PATH)
        os.rename(CACHE_FILE_PATH, f"{root}-{time.time():.0f}.{ext}")
        logger.exception("Failed to parse the cache file. A new one will be created.")


def getCacheKey(key: str) -> Any:
    return cache.get(key)


def setCacheKey(key: str, value: Any) -> None:
    cache[key] = value
    try:
        with open(CACHE_FILE_PATH, "w", encoding="UTF-8") as cacheFile:
            json.dump(cache, cacheFile, separators=(",", ":"))
    except:
        logger.exception("Failed to write to the cache file")


def getRecentGames() -> List[str]:
    recents = []
    if os.path.isfile(RECENTS_FILE_PATH):
        try:
            with open(RECENTS_FILE_PATH, "r", encoding="UTF-8") as recentsFile:
                recents = json.load(recentsFile)
        except:
            logger.exception("Failed to parse the recents file.")
    return recents


def setRecentGame(game: dict) -> None:
    recents = getRecentGames()
    game_name = normalize_game_name(
        game["name"]
    )  # assuming 'name' is a key in the game dict
    if game_name not in recents:
        recents.append(game_name)
    if len(recents) > 5:
        recents.pop(0)  # remove the oldest game
    try:
        with open(RECENTS_FILE_PATH, "w", encoding="UTF-8") as recentsFile:
            json.dump(recents, recentsFile, separators=(",", ":"))
    except:
        logger.exception("Failed to write to the recents file")
