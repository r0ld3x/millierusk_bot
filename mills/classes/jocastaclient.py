from abc import abstractmethod
import asyncio
import logging , os
from sqlite3 import OperationalError
import sys
import time
from telethon import TelegramClient, utils, errors
from mills.func.FastTelethon import download_file


from mills.utils.logger import log
from mills.config import get_str, get_int, del_key




class JocastaClient(TelegramClient):
    
    def __init__(
        self,
        session_name: str = "Millie",
        api_id: int = None,
        api_hash: str = None,
        bot_token: str = None,
        logger: logging.Logger = log,
        *args,
        **kwargs
        ):
        self._cache = {}
        self.logger = logger
        kwargs['api_id'] = api_id or get_int("API_ID")
        kwargs['api_hash'] = api_hash or get_str("API_HASH")
        try:
            super().__init__(session_name, **kwargs)
        except Exception as ex:
            logger.exception(f"Failed to initialize TelegramClient: {ex}")
            sys.exit(1)
        self.bot_token = bot_token 
        self.run(self.start_client(bot_token=self.bot_token))
        self.dc_id = self.session.dc_id
        self.logger.info(f"Using DC {self.dc_id}")
        
    
    async def start_client(self, **kwargs):
        """Start Bot Client
        """
        self.logger.info(f"Starting client")
        try:
            await self.start(**kwargs)
        except errors.TakeoutInitDelayError  as e:
            self.logger.exception("Must wait for {0} seconds before starting".format(e.seconds))
            time.sleep(e.seconds + 10)
            await asyncio.sleep(e.seconds + 10)
        except errors.AccessTokenExpiredError or errors.AccessTokenInvalidError:
            del_key("BOT_TOKEN")
            self.logger.error(
                "Bot token expired or Revoked. Create new from @Botfather and add in BOT_TOKEN env variable!"
            )
            sys.exit()
        except OperationalError as e:
            await self.connect()
        except Exception as e:
            self.logger.error("Unknown error occured while starting client: {0}".format(e))
            sys.exit()

        self.me = await self.get_me()
        self.parse_mode = 'html'
        self.logger.info("Logged In as {}".format(self.me.first_name))
    
    def run(self, func):
        """
        Run until get complete
        """
        self.loop.run_until_complete(func)
    

    def rud(self):
        """
        Run until get disconnected
        """
        return self.run_until_disconnected()
    
    
    def add_handler(self, func, *args, **kwargs):
        
        for x, y in self.list_event_handlers():
            if x == func:
                return False
            self.add_event_handler(func, *args, **kwargs)
    
    
    @property
    def utils(self):
        return utils
    
    @property
    def __dict__(self):
        return self.me.to_dict()

    @property
    def botname(self):
        """get botname of the bot

        Returns:
            str: botname of the bot
        """
        return self.me.username
    
    
    
    @property
    def botid(self):
        """get id of the bot

        Returns:
            str: id of the bot
        """
        return self.me.id
    
    
    @property
    def name(self):
        """get full name of the bot

        Returns:
            str: full name of the bot
        """
        return self.utils.get_display_name(self.me)


    async def fast_uploader(self, file, **kwargs):
        """Upload files in a faster way"""

        import os
        from pathlib import Path

        start_time = time.time()
        path = Path(file)
        filename = kwargs.get("filename", path.name)
        # Set to True and pass event to show progress bar.
        show_progress = kwargs.get("show_progress", False)
        if show_progress:
            event = kwargs["event"]
        # Whether to use cached file for uploading or not
        use_cache = kwargs.get("use_cache", True)
        # Delete original file after uploading
        to_delete = kwargs.get("to_delete", False)
        message = kwargs.get("message", f"Uploading {filename}...")
        by_bot = self._bot
        size = os.path.getsize(file)
        # Don't show progress bar when file size is less than 5MB.
        if size < 5 * 2**20:
            show_progress = False
        if use_cache and self._cache and self._cache.get("upload_cache"):
            for files in self._cache["upload_cache"]:
                if (
                    files["size"] == size
                    and files["path"] == path
                    and files["name"] == filename
                    and files["by_bot"] == by_bot
                ):
                    if to_delete:
                        try:
                            os.remove(file)
                        except FileNotFoundError:
                            pass
                    return files["raw_file"], time.time() - start_time
        from mills.func.FastTelethon import upload_file
        from mills.func.funcs import progress

        raw_file = None
        while not raw_file:
            with open(file, "rb") as f:
                raw_file = await upload_file(
                    client=self,
                    file=f,
                    filename=filename,
                    progress_callback=(
                        lambda completed, total: self.loop.create_task(
                            progress(completed, total, event, start_time, message)
                        )
                    )
                    if show_progress
                    else None,
                )
        cache = {
            "by_bot": by_bot,
            "size": size,
            "path": path,
            "name": filename,
            "raw_file": raw_file,
        }
        if self._cache.get("upload_cache"):
            self._cache["upload_cache"].append(cache)
        else:
            self._cache.update({"upload_cache": [cache]})
        if to_delete:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass
        return raw_file, time.time() - start_time


    async def fast_downloader(self, file, **kwargs):
        """Download files in a faster way"""
        # Set to True and pass event to show progress bar.
        show_progress = kwargs.get("show_progress", False)
        filename = kwargs.get("filename", None)
        if show_progress:
            event = kwargs["event"]
        # Don't show progress bar when file size is less than 10MB.
        if file.size < 10 * 2**20:
            show_progress = False
        import mimetypes

        from telethon.tl.types import DocumentAttributeFilename

        from mills.func.FastTelethon import upload_file
        from mills.func.funcs import progress

        start_time = time.time()
        # Auto-generate Filename
        if not filename:
            try:
                if isinstance(file.attributes[-1], DocumentAttributeFilename):
                    filename = file.attributes[-1].file_name
            except IndexError:
                mimetype = file.mime_type
                filename = (
                    mimetype.split("/")[0]
                    + "-"
                    + str(round(start_time))
                    + mimetypes.guess_extension(mimetype)
                )
        message = kwargs.get("message", f"Uploading {filename}...")

        raw_file = None
        while not raw_file:
            with open(filename, "wb") as f:
                raw_file = await download_file(
                    client=self,
                    location=file,
                    out=f,
                    progress_callback=(
                        lambda completed, total: self.loop.create_task(
                            progress(completed, total, event, start_time, message)
                        )
                    )
                    if show_progress
                    else None,
                )
        return raw_file, time.time() - start_time


    
    
