import sys
from typing import Any
import typing
from aioredis import Redis as r 
import os

from mills.utils.logger import log



class AioRedis(r):
    
    def __init__(self,
                host: str = None,
                port: int = None,
                password: str = None,
                logger=log,
                loop = None,
                encoding :str = 'utf-8',
                decode_responses = True,
                **kwargs
                ):
        if ':' in host:
            data = host.split(':')
            host = data[0]
            port = int(data[1])
        if host.startswith("http"):
            logger.error("Your REDIS_URI should not start with http!")
            sys.exit()
        elif not host or not port:
            logger.error("Port Number not found")
            sys.exit()
        kwargs["host"] = host
        if password :
            kwargs["password"] = password
        kwargs["port"] = port
        kwargs['encoding'] = encoding
        kwargs['decode_responses'] = decode_responses
        try:
            super().__init__(**kwargs)
        except Exception as e:
            logger.exception(f"Error while connecting to redis: {e}")
            sys.exit()
        self.loop = loop
        self.logger = logger
        self._cache = {}
        self.run(self.re_cache())
    
    async def re_cache(self):
        key = await self.keys()
        for keys in key:
            self._cache[keys] = await self.get(keys)
        self.logger.info("Cached {} keys".format(len(self._cache)))
    
    async def get_key(self, key: Any):
        if key in self._cache:
            try:
                return eval(self._cache[key]) 
            except: return self._cache[key]
        else:
            data =  await self.get(key)
            return eval(data) if data else None
        
    async def del_key(self, key: Any):
        if key in self._cache:
            del self._cache[key]
        return await self.delete(key)
    
    async def set_key(self, key: Any = None, value: Any = None):
        self._cache[key] = value
        return await self.set(key, value)
    
    def run(self, func):
        self.loop.run_until_complete(func)