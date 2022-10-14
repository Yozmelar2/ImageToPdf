import os
from PIL import Image
from pyrogram import Client,filters 
from pyrogram.types import (InlineKeyboardButton,  InlineKeyboardMarkup)

from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

TOKEN = os.environ.get("TOKEN", "5752725687:AAFEKJbf2yXwsvaFmWViQkK4bQK7ljy2yEo")

API_ID = int(os.environ.get("API_ID", 534493))

API_HASH = os.environ.get("API_HASH", "ac922823455e814e44020a9f3ee17914")
app = Client(
        "pdf",
        bot_token=TOKEN,api_hash=API_HASH,
            api_id=API_ID
    )


LIST = {}

@app.on_message(filters.command(['start']))
async def start(client, message):
 await message.reply_text(text =f"""Hello {message.from_user.first_name}  rasmni pdf qiluvchi bot

Menga rasmni yuboring
""",reply_to_message_id = message.message_id ,  reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Support 🇺🇿" ,url="https://t.me/Yozmelar") ],
                 [InlineKeyboardButton("", url="https://youtube.com/c/LNtechnical") ]       ]        ) )




@app.on_message(filters.private & filters.photo)
async def pdf(client,message):
 
 if not isinstance(LIST.get(message.from_user.id), list):
   LIST[message.from_user.id] = []

  
 
 file_id = str(message.photo.file_id)
 ms = await message.reply_text("PDF ga aylantirish ......")
 file = await client.download_media(file_id)
 
 image = Image.open(file)
 img = image.convert('RGB')
 LIST[message.from_user.id].append(img)
 await ms.edit(f"{len(LIST[message.from_user.id])} rasm Muvaffaqiyatli PDF yaratildi, agar siz koʻproq rasm qoʻshmoqchi boʻlsangiz, menga birma-bir yuboring.\n\n **Agar tayyor boʻlsa, shu yerni bosing 👉 /convert**")
 

@app.on_message(filters.command(['convert']))
async def done(client,message):
 images = LIST.get(message.from_user.id)

 if isinstance(images, list):
  del LIST[message.from_user.id]
 if not images:
  await message.reply_text( "Rasm yo'q !!")
  return

 path = f"{message.from_user.id}" + ".pdf"
 images[0].save(path, save_all = True, append_images = images[1:])
 
 await client.send_document(message.from_user.id, open(path, "rb"), caption = "Mana sizning pdf !!")
 os.remove(path)
 
 
 
 
app.run()
