from config.constants import CONFIG_FILE_PATH
from utils.dict import copyDict
from utils.logging import logger
import json
import models.config
import os
import time

config: models.config.Config = {
    "logging": {
        "debug": True,
        "writeToFile": False,
    },
    "display": {
        "hideTotalTime": False,
        "useRemainingTime": False,
        "posters": {
            "enabled": False,
            "imgurClientID": "",
        },
        "buttons": [],
    },
    "users": [],
}
supportedConfigFileExtensions = {
    "json": "json",
}
configFileExtension = ""
configFileType = ""
configFilePath = ""


def loadConfig() -> None:
    global configFileExtension, configFileType, configFilePath
    doesFileExist = False
    for i, (fileExtension, fileType) in enumerate(
        supportedConfigFileExtensions.items()
    ):
        doesFileExist = os.path.isfile(f"{CONFIG_FILE_PATH}")
        isFirstItem = i == 0
        if doesFileExist or isFirstItem:
            configFileExtension = fileExtension
            configFileType = fileType
            configFilePath = f"{CONFIG_FILE_PATH}"
            if doesFileExist:
                break
    if doesFileExist:
        try:
            with open(configFilePath, "r", encoding="UTF-8") as configFile:
                loadedConfig = json.load(configFile) or {}
        except:
            os.rename(
                configFilePath,
                f"{CONFIG_FILE_PATH}-{time.time():.0f}",
            )
            logger.exception(
                "Failed to parse the config file. A new one will be created."
            )
        else:
            copyDict(loadedConfig, config)
    saveConfig()


def saveConfig() -> None:
    try:
        with open(configFilePath, "w", encoding="UTF-8") as configFile:
            json.dump(config, configFile, indent="\t")
            configFile.write("\n")
    except:
        logger.exception("Failed to write to the config file")
