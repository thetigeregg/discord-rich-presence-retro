import os
import sys

NAME = "Discord Rich Presence for Retro"
VERSION = "0.0.1"

DISCORD_CLIENT_ID = "1172699413441949736"

DATA_DIRECTORY_PATH = "data"
CONFIG_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, "config.json")
RECENTS_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, "recents.json")
CACHE_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, "cache.json")
LOG_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, "console.log")
CSV_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, "games-list.csv")

IS_UNIX = sys.platform in ["linux", "darwin"]
PROCESS_ID = os.getpid()
IS_INTERACTIVE = sys.stdin and sys.stdin.isatty()

MODERN_PLATFORMS = [
    "PC (Microsoft Windows)",
    "PlayStation 4",
    "PlayStation 5",
    "Android",
    "Nintendo Switch",
]

REGION_LABELS = ["Japan", "Europe"]

PLATFORM_CLEAN_NAMES = {
    "Sega Mega Drive/Genesis": "Sega Genesis",
    "Super Nintendo Entertainment System (SNES)": "SNES",
    "Nintendo Entertainment System (NES)": "NES",
    "Family Computer Disk System": "Famicom Disk System",
    "Family Computer (FAMICOM)": "Famicom",
    "PC (Microsoft Windows)": "PC (Windows)",
    "Super Famicom": "SNES",
}
