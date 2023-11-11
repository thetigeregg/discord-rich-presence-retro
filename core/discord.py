from config.constants import DISCORD_CLIENT_ID, IS_UNIX, PROCESS_ID
from typing import Any, Optional
from utils.logging import logger
import asyncio
import json
import models.discord
import os
import struct
import time


class DiscordIpcService:
    def __init__(self, ipcPipeNumber: Optional[int]):
        ipcPipeNumber = ipcPipeNumber or -1
        ipcPipeNumbers = range(10) if ipcPipeNumber == -1 else [ipcPipeNumber]
        ipcPipeBase = (
            (
                "/run/app"
                if os.path.isdir("/run/app")
                else os.environ.get(
                    "XDG_RUNTIME_DIR",
                    os.environ.get(
                        "TMPDIR", os.environ.get("TMP", os.environ.get("TEMP", "/tmp"))
                    ),
                )
            )
            if IS_UNIX
            else r"\\?\pipe"
        )
        self.ipcPipes = [
            os.path.join(ipcPipeBase, f"discord-ipc-{ipcPipeNumber}")
            for ipcPipeNumber in ipcPipeNumbers
        ]
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.pipeReader: Optional[asyncio.StreamReader] = None
        self.pipeWriter: Optional[asyncio.StreamWriter] = None
        self.connected = False

    async def handshake(self) -> None:
        if not self.loop:
            return
        for ipcPipe in self.ipcPipes:
            try:
                if IS_UNIX:
                    (
                        self.pipeReader,
                        self.pipeWriter,
                    ) = await asyncio.open_unix_connection(
                        ipcPipe
                    )  # pyright: ignore[reportGeneralTypeIssues,reportUnknownMemberType]
                else:
                    self.pipeReader = asyncio.StreamReader()
                    self.pipeWriter = (
                        await self.loop.create_pipe_connection(
                            lambda: asyncio.StreamReaderProtocol(self.pipeReader),
                            ipcPipe,
                        )
                    )[
                        0
                    ]  # pyright: ignore[reportGeneralTypeIssues,reportUnknownMemberType]
                self.write(0, {"v": 1, "client_id": DISCORD_CLIENT_ID})
                if await self.read():
                    self.connected = True
                    logger.info(f"Connected to Discord IPC pipe {ipcPipe}")
                    break
            except FileNotFoundError:
                pass
            except:
                logger.exception(
                    f"An unexpected error occured while connecting to Discord IPC pipe {ipcPipe}"
                )
        if not self.connected:
            logger.error(
                f"Discord IPC pipe not found (attempted pipes: {', '.join(self.ipcPipes)})"
            )

    async def read(self) -> Optional[Any]:
        if not self.pipeReader:
            return
        try:
            dataBytes = await self.pipeReader.read(1024)
            data = json.loads(dataBytes[8:].decode("utf-8"))
            logger.debug("[READ] %s", data)
            return data
        except:
            logger.exception("An unexpected error occured during an IPC read operation")
            self.connected = False

    def write(self, op: int, payload: Any) -> None:
        if not self.pipeWriter:
            return
        try:
            logger.debug("[WRITE] %s", payload)
            payload = json.dumps(payload)
            self.pipeWriter.write(
                struct.pack("<ii", op, len(payload)) + payload.encode("utf-8")
            )
        except:
            logger.exception(
                "An unexpected error occured during an IPC write operation"
            )
            self.connected = False

    def connect(self) -> None:
        if self.connected:
            logger.warning(
                "Attempt to connect to Discord IPC pipe while already connected"
            )
            return
        logger.info("Connecting to Discord IPC pipe")
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.handshake())

    def disconnect(self) -> None:
        if not self.connected:
            logger.warning(
                "Attempt to disconnect from Discord IPC pipe while not connected"
            )
            return
        if not self.loop or not self.pipeWriter or not self.pipeReader:
            return
        logger.info("Disconnecting from Discord IPC pipe")
        try:
            self.pipeWriter.close()
        except:
            logger.exception(
                "An unexpected error occured while closing the IPC pipe writer"
            )
        try:
            self.loop.run_until_complete(self.pipeReader.read())
        except:
            logger.exception(
                "An unexpected error occured while closing the IPC pipe reader"
            )
        try:
            self.loop.close()
        except:
            logger.exception(
                "An unexpected error occured while closing the asyncio event loop"
            )
        self.connected = False

    def setActivity(self, activity: models.discord.Activity) -> None:
        if not self.connected:
            logger.warning(
                "Attempt to set activity while not connected to Discord IPC pipe"
            )
            return
        if not self.loop:
            return
        logger.info("Activity update: %s", activity)
        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": PROCESS_ID,
                "activity": activity,
            },
            "nonce": "{0:.2f}".format(time.time()),
        }
        self.write(1, payload)
        self.loop.run_until_complete(self.read())
