from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import aioschedule
import asyncio
import os
import random
import config

TOKEN = '6252011211:AAHguxl8iDx2AOz6xP4LD3V37Pb7Wa8usZc'
CHANNEL_ID = '@hot_Puppy'  # Идентификатор вашего канала
FOLDER_PATH = 'C:/Users/администратор/Desktop/photos'  # Путь к папке с файлами
interval = 60  # Интервал по умолчанию


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def send_message():
    try:
        files = os.listdir(FOLDER_PATH)
        if files:
            file_path = os.path.join(FOLDER_PATH, random.choice(files))
            file_extension = os.path.splitext(file_path)[1].lower()

            with open(file_path, 'rb') as f:
                if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                    await bot.send_photo(chat_id=CHANNEL_ID, photo=f)
                else:
                    await bot.send_document(chat_id=CHANNEL_ID, document=f)
        else:
            await bot.send_message(chat_id=CHANNEL_ID, text="Нет файлов для отправки.")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

async def scheduler(interval):
    while True:
        await send_message()
        await asyncio.sleep(interval * 60)

@dp.message_handler(commands=['setinterval'])
async def set_interval(message: types.Message):
    global interval
    try:
        new_interval = int(message.text.split()[1])
        if new_interval > 0:
            interval = new_interval
            await message.reply(f"Интервал публикации установлен на {interval} минут.")
        else:
            await message.reply("Пожалуйста, укажите положительное число.")
    except (IndexError, ValueError):
        await message.reply("Использование: /setinterval <минуты>")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Бот запущен!")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler(10))  # Установите интервал публикации
    executor.start_polling(dp, skip_updates=True)