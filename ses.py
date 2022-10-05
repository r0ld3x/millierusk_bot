import os

try:
    import telethon
except:
    os.system("pip install -U telethon")
    import telethon

from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession

print("""Session String Maker For Synergy.""")

API_ID: int = int(input("Enter your API ID: "))
API_HASH: str = str(input("Enter your API HASH: "))

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    try:
        session_string = client.session.save()
        client.send_message(
            "me",
            f"Your session string is:\n\n`{session_string}`",
        )
        print("Your session string is: {}".format(session_string))
    except Exception as e:
        print("Error while generating session: ", e)
