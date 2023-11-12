import os
import sys
from core.imgur import uploadToImgur
import models
from utils import prompt
from utils.parse import load_games_list
from utils.prompt import GameNameCompleter
from prompt_toolkit import prompt
import logging


from utils.text import (
    get_final_platform,
    get_final_region,
    get_year,
    normalize_game_name,
    sanitize_game_name,
    split_and_check,
)


try:
    import subprocess

    def parsePipPackages(packagesStr: str) -> dict[str, str]:
        return {
            packageSplit[0]: packageSplit[1] if len(packageSplit) > 1 else ""
            for packageSplit in [
                package.split("==") for package in packagesStr.splitlines()
            ]
        }

    pipFreezeResult = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )

    installedPackages = parsePipPackages(pipFreezeResult.stdout)

    with open("requirements.txt", "r", encoding="UTF-8") as requirementsFile:
        requiredPackages = parsePipPackages(requirementsFile.read())
    for packageName, packageVersion in requiredPackages.items():
        if packageName not in installedPackages:
            package = f"{packageName}{f'=={packageVersion}' if packageVersion else ''}"
            print(f"Installing missing dependency: {package}")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-U", package], check=True
            )
except Exception as e:
    import traceback

    traceback.print_exception(e)
    print(
        "An unexpected error occured during automatic installation of dependencies. Install them manually by running the following command: python -m pip install -U -r requirements.txt"
    )

from config.constants import (
    DATA_DIRECTORY_PATH,
    LOG_FILE_PATH,
    NAME,
    VERSION,
    IS_INTERACTIVE,
)
from core.config import config, loadConfig
from core.discord import DiscordIpcService
from utils.cache import (
    getCacheKey,
    loadCache,
    setCacheKey,
    setRecentGame,
    getRecentGames,
)
from utils.logging import logger, formatter
import logging
import time
from config.constants import REGION_LABELS
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory


def init() -> None:
    if not os.path.exists(DATA_DIRECTORY_PATH):
        os.mkdir(DATA_DIRECTORY_PATH)

    loadConfig()

    if config["logging"]["debug"]:
        logger.setLevel(logging.DEBUG)
    if config["logging"]["writeToFile"]:
        fileHandler = logging.FileHandler(LOG_FILE_PATH)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    logger.info("%s - v%s", NAME, VERSION)
    loadCache()


def main() -> None:
    init()

    games_dict = load_games_list()

    history = InMemoryHistory()

    recent_games = getRecentGames()
    if recent_games:
        for game_name in recent_games:
            history.append_string(game_name)

    game_name_completer = GameNameCompleter(games_dict)

    desired_game_name = prompt(
        "Please enter a game name: ", completer=game_name_completer, history=history
    )

    logger.info("%s: '%s'", "User selected game name", desired_game_name)

    normalized_game_name = normalize_game_name(desired_game_name)

    logger.info("%s: '%s'", "Normalized", normalized_game_name)

    game_data = games_dict[normalized_game_name]

    logger.debug("\n\n%s: '%s'\n", "Selected game data", game_data)

    start_time = int(time.time())

    logger.debug("%s: '%s'", "Start time", start_time)

    region_for_display = get_final_region(game_data["labels"])

    logger.info("%s: '%s'", "Region for display", region_for_display)

    platform_for_display = get_final_platform(game_data, region_for_display)

    logger.info("%s: '%s'", "Platform for display", platform_for_display)

    year = get_year(game_data["release_date"])

    logger.info("%s: '%s'", "Game release year", year)

    if year:
        if region_for_display:
            state_display = (
                platform_for_display + " (" + year + ", " + region_for_display + ")"
            )
        else:
            state_display = platform_for_display + " (" + year + ")"
    else:
        state_display = platform_for_display

    logger.info("%s: '%s'", "State for activity", state_display)

    image_key = sanitize_game_name(game_data["name"] + "_" + game_data["platform"])

    logger.info("%s: '%s'", "Image key", image_key)

    thumb_url_raw = game_data["image_url_medium"]

    logger.info("%s: '%s'", "Original image URL", thumb_url_raw)

    thumb_url_imgur = ""

    if image_key and thumb_url_raw and config["display"]["posters"]["enabled"]:
        thumb_url_imgur = getCacheKey(image_key)

        logger.info("%s: '%s'", "Imgur image URL from cache", thumb_url_imgur)

        if not thumb_url_imgur:
            logger.debug("Uploading image to Imgur")

            thumb_url_imgur = uploadToImgur(thumb_url_raw)

            logger.info("%s: '%s'", "Imgur image URL after upload", thumb_url_imgur)

            if thumb_url_imgur is not None:
                setCacheKey(image_key, thumb_url_imgur)

    activity: models.discord.Activity = {
        "details": game_data["name"],
        "state": state_display,
        "assets": {"large_image": thumb_url_imgur or "logo"},
        "timestamps": {"start": round(start_time)},
    }

    logger.info("%s: '%s'", "Final Discord activity", activity)

    discordIpcService = DiscordIpcService(-1)

    if not discordIpcService.connected:
        discordIpcService.connect()
    if discordIpcService.connected:
        discordIpcService.setActivity(activity)
        setRecentGame(game_data)

    while True:  # Keep the script running
        time.sleep(15)


def testIpc(ipcPipeNumber: int) -> None:
    init()

    logger.info("Testing Discord IPC connection")

    discordIpcService = DiscordIpcService(ipcPipeNumber)
    discordIpcService.connect()

    discordIpcService.setActivity(
        {
            "details": "details",
            "state": "state",
            "assets": {
                "large_text": "large_text",
                "large_image": "logo",
                "small_text": "small_text",
                "small_image": "playing",
            },
        }
    )

    time.sleep(15)

    discordIpcService.disconnect()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""

    try:
        if not mode:
            main()
        elif mode == "test-ipc":
            testIpc(int(sys.argv[2]) if len(sys.argv) > 2 else -1)
        else:
            print(f"Invalid mode: {mode}")
    except KeyboardInterrupt:
        pass
