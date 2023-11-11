import os
import sys


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
    dataDirectoryPath,
    logFilePath,
    name,
    version,
    isInteractive,
)
from core.config import config, loadConfig
from core.discord import DiscordIpcService
from core.plex import PlexAlertListener
from utils.cache import loadCache
from utils.logging import logger, formatter
import logging
import time


def init() -> None:
    if not os.path.exists(dataDirectoryPath):
        os.mkdir(dataDirectoryPath)

    for oldFilePath in ["config.json", "cache.json", "console.log"]:
        if os.path.isfile(oldFilePath):
            os.rename(oldFilePath, os.path.join(dataDirectoryPath, oldFilePath))

    loadConfig()

    if config["logging"]["debug"]:
        logger.setLevel(logging.DEBUG)
    if config["logging"]["writeToFile"]:
        fileHandler = logging.FileHandler(logFilePath)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    logger.info("%s - v%s", name, version)
    loadCache()


def main() -> None:
    init()

    # plexAlertListener = PlexAlertListener()

    game_name_completer = GameNameCompleter()
    desired_game_name = prompt(
        "Please enter a game name: ", completer=game_name_completer
    )
    game_data = load_games_list()[normalize_game_name(desired_game_name)]
    set_discord_presence(game_data)
    while True:  # Keep the script running
        time.sleep(15)

    try:
        if isInteractive:
            while True:
                userInput = input()
                if userInput in ["exit", "quit"]:
                    raise KeyboardInterrupt
        else:
            while True:
                time.sleep(3600)
    except KeyboardInterrupt:
        plexAlertListener.disconnect()


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
