
from time import strftime, gmtime


from mills import mdb
from mills.utils.logger import log


async def user_info(m):
    """get user info from server."""
    user_info = await mdb.find_one('users', {'_id': m.sender_id})
    if not user_info:
        sender = await m.get_sender()
        upload = {
            '_id': m.sender_id,
            'username': sender.username if hasattr(sender,'username') else None,
            'type': 'F',
            'created': strftime("%Y-%m-%d", gmtime()),
            'role': 'Free',
            'credits': 0,
            'antispam': True,
            'antispam_time': 60,
            'saveccs': True,
            'keys': [],
            'claimed_date': [],
            'lives': [],
        }
        x = await m.mdb.insert_one('users', upload)
        if x :
            user_info = await mdb.find_one('users', {'_id': m.sender_id})
            if user_info:
                return user_info
        return False
    return user_info



def get_user_info():
    """get user info."""
    def strings(func):
        async def wrap(*args, **kwargs):
            m = args[0]
            _ = await user_info(m)
            if _:
                await func(*args,_, **kwargs)
            else:
                await m.sod("Error While Getting User Info", time = 5)
                return
        return wrap
    return strings
