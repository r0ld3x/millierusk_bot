from abc import abstractmethod
import asyncio
import logging , os
import sys
import time
from telethon import TelegramClient, utils, errors


from mills.utils.logger import log
from mills.config import get_str, get_int, del_key




class UserClient(TelegramClient):
    
    def __init__(
        self,
        session_name,
        api_id: int = None,
        api_hash: str = None,
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
        # self.bot_token = bot_token or get_str("BOT_TOKEN")
        self.run(self.start_client())
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
        except Exception as e:
            self.logger.error("Unknown error occured while starting client: {0}".format(e))
            sys.exit()

        self.me = await self.get_me()
        self.logger.info("Logged In as {}".format(self.me.first_name))
    
    
    def run(self, func):
        """
        Run until get disconnected
        """
        self.loop.run_until_complete(func)
    

    def rud(self):
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
    def username(self):
        """get username of the user

        Returns:
            str: username of the user
        """
        return self.me.username
    
    
    
    @property
    def userid(self):
        """get id of the user

        Returns:
            str: id of the user
        """
        return self.me.id
    
    
    @property
    def name(self):
        """get full name of the user

        Returns:
            str: full name of the user
        """
        return self.utils.get_display_name(self.me)
    
    

    
    
