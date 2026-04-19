import asyncio
import logging
import aiohttp

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


BOT_TOKEN = "8344336191:AAFrAj60650Jx1p8ayNlByI40rfnZztUc7Y"

API_URL = "http://localhost:8000/auth/send-otp/"


logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Send phone number", request_contact=True)]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, command):
    session_id = command.args

    if not session_id:
        await message.answer("Invalid link ❌")
        return


    await state.update_data(session_id=session_id)

    await message.answer(
        "📲 Please send your phone number",
        reply_markup=contact_keyboard
    )


@dp.message(F.contact)
async def contact_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    session_id = data.get("session_id")

    if not session_id:
        await message.answer("Session not found ❌")
        return

    phone = message.contact.phone_number
    telegram_id = message.from_user.id

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                API_URL,
                json={
                    "phone": phone,
                    "session_id": session_id,
                    "telegram_id": telegram_id
                }
            ) as response:

                
                text = await response.text()
                print("RESPONSE STATUS:", response.status)
                print("RESPONSE TEXT:", text)

               
                if response.status != 200:
                    await message.answer(f"❌ Backend error: {response.status}")
                    return

                
                try:
                    result = await response.json()
                except:
                    await message.answer("❌ Invalid response from server")
                    return

        if result.get("status") == "ok":
            otp = result.get("otp")
            await message.answer(f"🔐 Your OTP code: {otp}")
        else:
            await message.answer("❌ Failed to get OTP")

    except Exception as e:
        await message.answer(f"⚠️ Error: {e}")
        print("ERROR:", e)
        

@dp.message()
async def fallback(message: Message):
    await message.answer("Please use /start and send phone number 📱")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())