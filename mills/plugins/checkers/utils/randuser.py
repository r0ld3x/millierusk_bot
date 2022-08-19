import time
import os , re , sys

from mills import adb , mdb
from mills.utils.logger import log


from mills import user_info


def rand_user_dec():
    """get gate info."""
    def inner(func):
        async def wrap(*args, **kwargs):
            m = args[0]
            _ = user_info.rand_user()
            try:
                await func(*args,_,**kwargs)
            except Exception as er:
                await m.sod(er)
        return wrap
    return inner
