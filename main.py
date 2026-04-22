import pip
import os
import sys

try:
    import aiogram, gtts, aioschedule, pip
except ModuleNotFoundError:
    print("Установка дополнений...")
    pip.main(['install', 'aiogram==2.25'])
    pip.main(['install', 'gtts'])
    pip.main(['install', 'aioschedule'])
    pip.main(['install', 'telebot'])
    python.exe(['-m pip install', 'pip'])
    python.exe(['--upgrade pip', 'pip'])

    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()

# Импорты
import logging
from aiogram import types
from aiogram.utils import executor
from format_text import start_message0, start_message, start_message2, start_message3, start_message4
from format_text import start_message5, start_message6, start_message7, start_message8, start_message9
from format_text import start_message10, start_message11, start_message12, start_message13, start_message14
from media import register_handlers
import markups as nav
from admins import bot, dp, register_hendlers_admin, admin_id
import text_loader
import config
import os
import random
import telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
from db import Database
import asyncio
CHANNEL_ID = '@hot_Puppy'  # Идентификатор вашего канала
FOLDER_PATH = 'C:/Users/администратор/Desktop/photos'  # Путь к папке с файлами
db = Database('user_db.db')
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger.info("Starting bot\n"
            f'made by: KELPIX\n'
            f'██╗  ██╗███████╗██╗     ██████╗ ██╗██╗  ██╗\n'
            f'██║ ██╔╝██╔════╝██║     ██╔══██╗██║╚██╗██╔╝\n'
            f'█████╔╝ █████╗  ██║     ██████╔╝██║ ╚███╔╝ \n'
            f'██╔═██╗ ██╔══╝  ██║     ██╔═══╝ ██║ ██╔██╗ \n'
            f'██║  ██╗███████╗███████╗██║     ██║██╔╝ ██╗\n'
            f'╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝\n'
            f'made by: MADE in UA\n')
TOKEN1 = '6021752192:AAG5BXBDlQoc75QAFn6HM3dnXxhfDofB5xk'
app = ApplicationBuilder().token(TOKEN1).build()
async def send_message():
    try:
        files = os.listdir(FOLDER_PATH)
        if files:
            file_path = os.path.join(FOLDER_PATH, random.choice(files))
            file_extension = os.path.splitext(file_path)[1].lower()

            with open(file_path, 'rb') as f:
                if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                    await app.bot.send_photo(chat_id=CHANNEL_ID, photo=f)
                else:
                    await app.bot.send_document(chat_id=CHANNEL_ID, document=f)
        else:
            await app.bot.send_message(chat_id=CHANNEL_ID, text="Нет файлов для отправки.")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

async def scheduler(interval):
    while True:
        await send_message()
        await asyncio.sleep(interval * 60)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен!")


@dp.message_handler(text='Керування автопостом')
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_1_min = InlineKeyboardButton("Установить интервал 1 мин", callback_data='set_interval_1')
    button_5_min = InlineKeyboardButton("Установить интервал 5 мин", callback_data='set_interval_5')
    button_10_min = InlineKeyboardButton("Установить интервал 10 мин", callback_data='set_interval_10')
    keyboard.add(button_1_min, button_5_min, button_10_min)

    await message.reply("Выберите интервал публикации:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('set_interval_'))
async def process_callback_set_interval(callback_query: types.CallbackQuery):
    global interval
    interval_map = {
        'set_interval_1': 1,
        'set_interval_5': 5,
        'set_interval_10': 10
    }

    new_interval = interval_map.get(callback_query.data)
    if new_interval:
        interval = new_interval
        await bot.answer_callback_query(callback_query.id, text=f"Интервал публикации установлен на {interval} минут.")
    else:
        await bot.answer_callback_query(callback_query.id, text="Не удалось установить интервал.")


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is False:
            db.set_nickname(message.from_user.id, message.from_user.first_name)
            db.add_user(message.from_user.id, message.from_user.first_name)
            await bot.send_message(message.chat.id, '*Привіт, бот стане доступним після покупки передплати!*\!',
                                   reply_markup=nav.userMenu, parse_mode="MarkdownV2")
        elif db.user_exists(message.from_user.id) is True:
            db.set_nickname(message.from_user.id, message.from_user.first_name)

            if db.admin_status(message.from_user.id) == True:
                await bot.send_message(message.from_user.id,
                                       f'З поверненням {message.from_user.first_name} \n {start_message}',
                                       reply_markup=nav.OSNMenu)  # Администратор
                # С возращением + ник
            elif db.moder_status(message.from_user.id) == True:
                await bot.send_message(message.from_user.id,
                                       f'С возвращением {message.from_user.first_name}\n {start_message2}',
                                       reply_markup=nav.moderMenu)  # MODER
            else:
                # Клавиатура для обычных юзеров
                await bot.send_message(message.from_user.id,
                                       f'Вітаю тебе "{message.from_user.first_name}"\n {start_message0}',
                                       reply_markup=nav.userMenu)


@dp.message_handler(text='Керування функціями')
async def mainMenu(message: types.Message):
    if message.chat.type == 'private':
        db.set_nickname(message.from_user.id, message.from_user.first_name)
        if db.admin_status(message.from_user.id) == 1:
            # Панель Администратора
            await bot.send_message(message.from_user.id, f'{start_message13}', reply_markup=nav.mainMenu)
        elif db.moder_status(message.from_user.id) == 1:
            # Панель для Модератора
            await bot.send_message(message.from_user.id, f'{start_message13}', reply_markup=nav.moderMenu)
        elif db.admin_status(message.from_user.id) == 0 and message.from_user.id == admin_id:
            db.set_admin(message.from_user.id)
            await bot.send_message(message.from_user.id, f'{start_message}', reply_markup=nav.mainMenu)
        else:
            #  Звичайному користовачу
            await bot.send_message(message.from_user.id, f'{start_message6}')


@dp.message_handler(text='Головна сторінка')  # Повернутися на головну сторінку
async def info(message: types.Message):
    if message.chat.type == 'private':
        db.set_nickname(message.from_user.id, message.from_user.first_name)
        if db.admin_status(message.from_user.id) == 1:
            # Панель Администратора
            await bot.send_message(message.from_user.id, f'{start_message14}', reply_markup=nav.OSNMenu)
        elif db.moder_status(message.from_user.id) == 1:
            # Панель для Модератора
            await bot.send_message(message.from_user.id, f'{start_message2}', reply_markup=nav.moderMenu)
        elif db.admin_status(message.from_user.id) == 0 and message.from_user.id == admin_id:
            db.set_admin(message.from_user.id)
            await bot.send_message(message.from_user.id, f'{start_message}', reply_markup=nav.mainMenu)
        else:
            #  Звичайному користовачу
            await bot.send_message(message.from_user.id, f'{start_message6}')


@dp.message_handler(commands=['init'])
async def check(message: types.Message):
    if message.chat.type == 'group' or 'supergroup' or 'channel':
        db.add_private_channel(message.chat.id, message.from_user.id)
        try:
            await bot.send_message(message.from_user.id, '*Чат доданий*\!', parse_mode='MarkdownV2')
        except Exception as ex:
            print(f'Неможливо отримати айді для надсилання повідомлення {ex}')


@dp.message_handler(text='Допомога')
async def help(message: types.Message):
    if message.chat.type == 'private':
        db.set_nickname(message.from_user.id, message.from_user.first_name)
        if db.admin_status(message.from_user.id) == 1:
            # ADMIN
            await bot.send_message(message.from_user.id, f'{start_message4}', reply_markup=nav.mainMenu)
        elif db.moder_status(message.from_user.id) == 1:
            # MODER
            await bot.send_message(message.from_user.id, f'{start_message5}', reply_markup=nav.moderMenu)
        elif db.admin_status(message.from_user.id) == 0 and message.from_user.id == admin_id:
            db.set_admin(message.from_user.id)
            await bot.send_message(message.from_user.id, f'{start_message}', reply_markup=nav.mainMenu)
        else:
            # Помощь юзеру
            await bot.send_message(message.from_user.id, f'{start_message6}')


@dp.message_handler(text='Графік публікацій')  # График публикаций постов
async def grafic(message: types.Message):
    if message.chat.type == 'private':
        db.set_nickname(message.from_user.id, message.from_user.first_name)
        if db.admin_status(message.from_user.id) == 1:  # ADMIN
            await bot.send_message(message.from_user.id, f'{start_message11}')
        elif db.moder_status(message.from_user.id) == 1:  # MODER
            await bot.send_message(message.from_user.id, f'{start_message11}')
        elif db.admin_status(message.from_user.id) == 0 and message.from_user.id == admin_id:
            db.set_admin(message.from_user.id)
            await bot.send_message(message.from_user.id, f'{start_message}')
        else:  # USER
            await bot.send_message(message.from_user.id, f'{start_message11}', reply_markup=nav.userMenu)


@dp.message_handler(text='Інфо')  # Инфо + Помощь
async def info(message: types.Message):
    if message.chat.type == 'private':
        db.set_nickname(message.from_user.id, message.from_user.first_name)
        if db.admin_status(message.from_user.id) == 1:  # ADMIN
            # ADMIN
            await bot.send_message(message.from_user.id, f'{start_message3}')
        elif db.moder_status(message.from_user.id) == 1:  # MODER
            # MODER
            await bot.send_message(message.from_user.id, f'{start_message3}')
        elif db.admin_status(message.from_user.id) == 0 and message.from_user.id == admin_id:
            db.set_admin(message.from_user.id)
            await bot.send_message(message.from_user.id, f'{start_message}')
        else:  # USER
            await bot.send_message(message.from_user.id, f'{start_message3}', reply_markup=nav.userMenu)


@dp.message_handler(text='Новини')  # Инфо
async def info(message: types.Message):
    if message.chat.type == 'private':
        db.set_nickname(message.from_user.id, message.from_user.first_name)
        if db.admin_status(message.from_user.id) == 1:  # ADMIN
            # ADMIN
            await bot.send_message(message.from_user.id, f'{start_message7}')
        elif db.moder_status(message.from_user.id) == 1:  # MODER
            # MODER
            await bot.send_message(message.from_user.id, f'{start_message7}')
        elif db.admin_status(message.from_user.id) == 0 and message.from_user.id == admin_id:
            db.set_admin(message.from_user.id)
            await bot.send_message(message.from_user.id, f'{start_message}')
        else:  # USER
            await bot.send_message(message.from_user.id, f'{start_message7}', reply_markup=nav.userMenu)


@dp.message_handler(text='Замовити Рекламу')  # Оформлення замовлення
async def menu_in(message: types.Message):
    if message.chat.type == 'private':
        db.set_nickname(message.from_user.id, message.from_user.first_name)
        if db.admin_status(message.from_user.id) == 1:  # ADMIN
            # ADMIN
            await bot.send_message(message.from_user.id, f'{start_message8}', reply_markup=nav.partnersMenu)
        elif db.moder_status(message.from_user.id) == 1:  # MODER
            # MODER
            await bot.send_message(message.from_user.id, f'{start_message8}', reply_markup=nav.partnersMenu)
        elif db.admin_status(message.from_user.id) == 0 and message.from_user.id == admin_id:
            db.set_admin(message.from_user.id)
            await bot.send_message(message.from_user.id, f'{start_message}')
        else:  # USER
            await bot.send_message(message.from_user.id, f'{start_message8}', reply_markup=nav.partnersMenu)


@dp.message_handler(text='Замовити Хостинг')  # Оформлення замовлення
async def host_shopMenu(message: types.Message):
    if message.chat.type == 'private':
        db.set_nickname(message.from_user.id, message.from_user.first_name)
        if db.admin_status(message.from_user.id) == 1:  # ADMIN
            # ADMIN
            await bot.send_message(message.from_user.id, f'{start_message8}', reply_markup=nav.host_shopMenu)
        elif db.moder_status(message.from_user.id) == 1:  # MODER
            # MODER
            await bot.send_message(message.from_user.id, f'{start_message8}', reply_markup=nav.host_shopMenu)
        elif db.admin_status(message.from_user.id) == 0 and message.from_user.id == admin_id:
            db.set_admin(message.from_user.id)
            await bot.send_message(message.from_user.id, f'{start_message}')
        else:  # USER
            await bot.send_message(message.from_user.id, f'{start_message8}', reply_markup=nav.host_shopMenu)


@dp.message_handler(text='Назад')  #
async def Back_in(message: types.Message):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is False:
            db.set_nickname(message.from_user.id, message.from_user.first_name)
            db.add_user(message.from_user.id, message.from_user.first_name)
            await bot.send_message(message.chat.id, '*Привіт, бот стане доступним після покупки передплати!*\!',
                                   reply_markup=nav.userMenu, parse_mode="MarkdownV2")
        elif db.user_exists(message.from_user.id) is True:
            db.set_nickname(message.from_user.id, message.from_user.first_name)

            if db.admin_status(message.from_user.id) == True:
                await bot.send_message(message.from_user.id,
                                       f'З поверненням {message.from_user.first_name} \n {start_message}',
                                       # С возращением + ник
                                       reply_markup=nav.OSNMenu)  # ADMIN (Кновки + инфо панель)
            elif db.moder_status(message.from_user.id) == True:
                await bot.send_message(message.from_user.id,
                                       f'С возвращением {message.from_user.first_name}\n {start_message2}',
                                       reply_markup=nav.moderMenu)  # MODER
            else:
                # Клавиатура для обычных юзеров
                await bot.send_message(message.from_user.id,
                                       f'Вітаю тебе "{message.from_user.first_name}"\n {start_message12}',
                                       reply_markup=nav.userMenu)


@dp.message_handler(text='1 Місяць')
async def shop(message: types.Message):
    try:
        print(f"Payment Token: {config.payment_token}")  # Вывод токена для проверки
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Замовлення реклами на 1 Місяць',
            description='Покупка реклами від Father List',
            payload='invoice',
            provider_token=config.payment_token,
            currency='UAH',
            prices=[types.LabeledPrice('Покупка реклами', 10000)]  # цена в копейках (100 UAH = 10000 копеек)
        )
    except Exception as e:
        print(f"Error sending invoice: {e}")


@dp.message_handler(text='3 Місяці')
async def shop(message: types.Message):
    try:
        print(f"Payment Token: {config.payment_token}")  # Вывод токена для проверки
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Замовлення реклами на 3 Місяці',
            description='Покупка реклами від Father List',
            payload='invoice',
            provider_token=config.payment_token,
            currency='UAH',
            prices=[types.LabeledPrice('Покупка реклами', 50000)]  # цена в копейках (1 UAH = 50000 копеек)
        )
    except Exception as e:
        print(f"Error sending invoice: {e}")


@dp.message_handler(text='6 Місяців')
async def shop(message: types.Message):
    try:
        print(f"Payment Token: {config.payment_token}")  # Вывод токена для проверки
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Замовлення реклами на 6 Місяців ',
            description='Покупка реклами від Father List',
            payload='invoice',
            provider_token=config.payment_token,
            currency='UAH',
            prices=[types.LabeledPrice('Покупка реклами', 100000)]  # цена в копейках (1000 UAH  копеек 100000)
        )
    except Exception as e:
        print(f"Error sending invoice: {e}")


@dp.message_handler(text='12 Місяців')
async def shop(message: types.Message):
    try:
        print(f"Payment Token: {config.payment_token}")  # Вывод токена для проверки
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Замовлення реклами на 12 Місяців',
            description='Покупка реклами від Father List',
            payload='invoice',
            provider_token=config.payment_token,
            currency='UAH',
            prices=[types.LabeledPrice('Покупка реклами', 150000)]  # цена в копейках (1000 UAH  копеек 100000)
        )
    except Exception as e:
        print(f"Error sending invoice: {e}")


@dp.message_handler(text='1 Місяць Оренди')
async def shop(message: types.Message):
    try:
        print(f"Payment Token: {config.payment_token}")  # Вывод токена для проверки
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Замовлення хостингу на 1 Місяць',
            description='Покупка Father List',
            payload='invoice',
            provider_token=config.payment_token,
            currency='UAH',
            prices=[types.LabeledPrice('Замовлення хостинга від Father List', 39000)]
            # цена в копейках (100 UAH = 10000 копеек)
        )
    except Exception as e:
        print(f"Error sending invoice: {e}")


@dp.message_handler(text='3 Місяці Оренди')
async def shop(message: types.Message):
    try:
        print(f"Payment Token: {config.payment_token}")  # Вывод токена для проверки
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Замовлення хостингу на 3 Місяця',
            description='Покупка Father List',
            payload='invoice',
            provider_token=config.payment_token,
            currency='UAH',
            prices=[types.LabeledPrice('Замовлення хостинга від Father List', 70000)]
            # цена в копейках (1 UAH = 50000 копеек)
        )
    except Exception as e:
        print(f"Error sending invoice: {e}")


@dp.message_handler(text='6 Місяців Оренди')
async def shop(message: types.Message):
    try:
        print(f"Payment Token: {config.payment_token}")  # Вывод токена для проверки
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Замовлення хостингу на 6 Місяців',
            description='Покупка Father List',
            payload='invoice',
            provider_token=config.payment_token,
            currency='UAH',
            prices=[types.LabeledPrice('Замовлення хостинга від Father List', 120000)]
            # цена в копейках (1000 UAH  копеек 100000)
        )
    except Exception as e:
        print(f"Error sending invoice: {e}")


@dp.message_handler(text='12 Місяців Оренди')
async def shop(message: types.Message):
    try:
        print(f"Payment Token: {config.payment_token}")  # Вывод токена для проверки
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Замовлення хостингу на 12 Місяців',
            description='Покупка Father List',
            payload='invoice',
            provider_token=config.payment_token,
            currency='UAH',
            prices=[types.LabeledPrice('Замовлення хостинга від Father List', 180000)]
            # цена в копейках (1000 UAH  копеек 100000)
        )
    except Exception as e:
        print(f"Error sending invoice: {e}")


@dp.message_handler(text='Тарифи')
async def shop(message: types.Message):
    if message.chat.type == 'private':
        db.set_nickname(message.from_user.id, message.from_user.first_name)
        if db.admin_status(message.from_user.id) == 1:  # ADMIN
            # ADMIN
            await bot.send_message(message.from_user.id, f'{start_message10}')
        elif db.moder_status(message.from_user.id) == 1:  # MODER
            # MODER
            await bot.send_message(message.from_user.id, f'{start_message10}')
        elif db.admin_status(message.from_user.id) == 0 and message.from_user.id == admin_id:
            db.set_admin(message.from_user.id)
            await bot.send_message(message.from_user.id, f'{start_message}')
        else:  # USER
            await bot.send_message(message.from_user.id, f'{start_message10}')

# photo
"""
55
"""
#
text_loader.register_hendlers(dp)
register_hendlers_admin(dp)
register_handlers(dp)


async def on_startup(_):
    asyncio.create_task(text_loader.scheduler())
    if db.get_status_malling == 1:
        await bot.send_message(admin_id, 'Розсилка активна')


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.create_task(text_loader.periodic())
    app.add_handler(CommandHandler("start", start))
  #  app.add_handler(CommandHandler("setinterval", set_interval))
    interval = 60  # Интервал по умолчанию в минутах

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler(interval))

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    # asyncio.run(text_loader.periodic())
    # asyncio.run(main())