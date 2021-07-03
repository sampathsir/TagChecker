from pyrogram import filters, Client
import logging
import os
from pyrogram.types import (
   ChatPermissions,
   InlineKeyboardButton,
   InlineKeyboardMarkup
)

logging.basicConfig(level=logging.INFO)

API_ID = int(os.environ.get("API_ID", 6))
API_HASH = os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
TOKEN = os.environ.get("TOKEN", None)
TAG = os.environ.get("TAG", None)
OWNER_ID = int(os.environ.get("OWNER_ID", 1704673514))


tagcheck = Client(
   "tagcheck",
   bot_token=TOKEN,
   api_id=API_ID,
   api_hash=API_HASH
)

user_s = {}

async def is_admin(message):
    user = await tagcheck.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in ("administrator", "creator"):
      return True
    return False

@tagcheck.on_message(filters.command("start") & filters.user(OWNER_ID))
async def start(_, message):
   await message.reply("I can Support on @Heavennetworks only.")

@tagcheck.on_message(filters.group)
async def tag_check(_, message):
    if await is_admin(message):
       return
    user = message.from_user.id
    if TAG not in message.from_user.last_name:
       await tagcheck.restrict_chat_member(
        message.chat.id,
        user,
        ChatPermissions(),
       )
       text = f"""
**Heya {message.from_user.mention}**
Please add our tag in your name to
chat again in the group.

**Tag:** `{TAG}`
**Note:** __Click The Below Button For
Unmuting YourSelf!__
"""
       await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Unmute Me", callback_data="unmute")]
           ]
         )
       )
       user_s.update({"user_id": user})

@tagcheck.on_callback_query(filters.regex("unmute"))
async def unmute(client, cb):
    try:
       user = user_s["user_id"]
    except KeyError:
      await cb.answer(
        "Oops!\nIts looks like i lost your id from my server\nContact Admins For Unmiting", 
        show_alert=True
      )
      return
    if cb.from_user.id != user:
      await cb.answer("This Button is not for you!", show_alert=True)
      return

    if TAG in cb.from_user.first_name:
      await tagcheck.unban_chat_member(cb.message.chat.id, user)
      await cb.answer("Succesfully Unmuted!")
      await message.delete()
      return
    await cb.answer("Please add tag in your name!", show_alert=True)


tagcheck.run()
