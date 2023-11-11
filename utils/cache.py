from .logging import logger
from config.constants import CACHE_FILE_PATH
from typing import Any
import json
import os
import time

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
