import sys
from typing import Any
import typing
from redis import Redis as r 
import os

from mills.utils.logger import log



class Redis(r):
    
    def __init__(self,
                host: str = None,
                port: int = None,
                password: str = None,
                logger=log,
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
        # kwargs['client_name'] = client_name
        # kwargs['username'] = username
        try:
            super().__init__(**kwargs)
        except Exception as e:
            logger.exception(f"Error while connecting to redis: {e}")
            sys.exit()
        self.logger = logger
        self._cache = {}
        self.re_cache()
    
    def re_cache(self):
        key = self.keys()
        for keys in key:
            self._cache[keys] = self.get(keys)
        self.logger.info("Cached {} keys".format(len(self._cache)))
    
    def get_key(self, key: Any):
        if key in self._cache:
            return self._cache[key]
        else:
            return self.get(key)
        
    def del_key(self, key: Any):
        if key in self._cache:
            del self._cache[key]
        return self.delete(key)
    
    def set_key(self, key: Any = None, value: Any = None):
        self._cache[key] = value
        return self.set(key, value)
    