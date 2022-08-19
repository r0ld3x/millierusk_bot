import time
from mills import ADMINS, adb , mdb
from mills.utils.logger import log
from requests.exceptions import ProxyError

from mills.plugins.checkers.utils.userinfo import user_info


def get_gate_info(cmd_name: str = None,is_shopify = False):
    """get gate info."""
    def strings(func):
        async def wrap(*args, **kwargs):
            m = args[0]
            user = await user_info(m)
            if not user:
                await m.sod("Error While Getting User Info", time = 5)
                return
            if user['type'] == "P":
                if user['expire_days'] < time.time():
                    await m.sod("Your Premium Plan has expired. Please contact @r0ld3x for renewing your plan.", time = 5)
                    await mdb.update_one('users',{'_id':m.sender_id},{'plan':"F",'role': "Free"})
                    return
                # elif user['expire_days'] - time.time() < 3600:
                #     await m.sod("Your Premium Plan will expire in 1 hour. Please contact @r0ld3x for renewing your plan.", time = 5)
                #     return
            else:
                if m.is_private:
                    await m.sod("you dont have to use this command in private chat. talk with @r0ld3x for access.", time = 5)
                    return
                all_chats = await m.adb.get_key(f'approved_{str(m.chat_id)}')
                if not m.is_private and not all_chats and m.sender_id not in ADMINS:
                    await m.sod("This chat is unauthorized to use this bot. Please contact @r0ld3x for more info.", time = 5)
                    return
            if is_shopify:
                if 'shopify_apis' in user:
                    if len(user['shopify_apis']) < 1:
                        return await m.sod("You have 0 Shopify APIs. Please contact @r0ld3x for more info.", time = 5)
                    api_name = m.pattern_match.group(1).split('|',maxsplit=1)[0].strip()
                    if not api_name.startswith('api') or not api_name in user['shopify_apis'].keys():
                        return await m.sod("Please use valid api names.", time = 5)
                    site = user['shopify_apis'].get(api_name, None)
                    if not site:
                        return await m.sod("Please use valid api names.", time = 5)
                    await func(*args,{'api_name':api_name,'api_site':site},user,**kwargs)
            if cmd_name:
                gate_info = await mdb.find_one('gate', str(cmd_name))
                if not gate_info:
                    await m.sod("{} gate not found.".format(cmd_name), time = 5)
                    return
                if user['antispam']:
                    antispam =  await adb.get_key(f'antispam_{str(m.sender_id)}')
                    if antispam:
                        sec = time.time() - antispam
                        if sec < user['antispam_time']:
                            await m.sod("You can use this command in {} seconds.".format(str(user['antispam_time'] -  sec)), time = 5)
                            return
                if gate_info['is_paid'] and user['type'] == "F":
                    return await m.sod("<b>This is a paid gate.You've to take premium to use this gate.</b>\n<i>Use /buy to check premium plans</i>.")
                try:
                    await func(*args,gate_info,user,**kwargs)
                except ProxyError:
                    await m.sod("Proxy Error. Please try again later.", time = 5)
        return wrap
    return strings
