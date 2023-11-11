import os
import sys

name = "Discord Rich Presence for Retro"
version = "0.0.1"

plexClientID = "discord-rich-presence-plex"
discordClientID = "413407336082833418"

dataDirectoryPath = "data"
configFilePathRoot = os.path.join(dataDirectoryPath, "config")
cacheFilePath = os.path.join(dataDirectoryPath, "cache.json")
logFilePath = os.path.join(dataDirectoryPath, "console.log")

isUnix = sys.platform in ["linux", "darwin"]
processID = os.getpid()
isInteractive = sys.stdin and sys.stdin.isatty()
containerDemotionUidGid = os.environ.get("DRPP_CONTAINER_DEMOTION_UID_GID", "")

modern_platforms = [
    "PC (Microsoft Windows)",
    "PlayStation 4",
    "PlayStation 5",
    "Android",
    "Nintendo Switch",
]
region_labels = ["Japan", "Europe"]
platform_clean_names = {
    "Sega Mega Drive/Genesis": "Sega Genesis",
    "Super Nintendo Entertainment System (SNES)": "SNES",
    "Nintendo Entertainment System (NES)": "NES",
    "Family Computer Disk System": "Famicom Disk System (NES)",
}
