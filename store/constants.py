import os
import sys

name = "Discord Rich Presence for Plex"
version = "2.3.5"

plexClientID = "discord-rich-presence-plex"
discordClientID = "413407336082833418"

dataFolderPath = "data"
configFilePath = os.path.join(dataFolderPath, "config.json")
cacheFilePath = os.path.join(dataFolderPath, "cache.json")
logFilePath = os.path.join(dataFolderPath, "console.log")

isUnix = sys.platform in ["linux", "darwin"]
processID = os.getpid()
