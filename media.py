from aiogram.types import ContentType, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher.filters import Regexp
from admins import dp, bot
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import markups as nav
from db import Database

db = Database('user_db.db')


class UrlLoader(StatesGroup):
    url_media = State()


async def load_media(message: Message):
    await message.answer('Скинь посилання на медіа')
    await UrlLoader.url_media.set()

async def handler_media(message: Message, state: FSMContext):
    async with state.proxy() as data: 
        data['media'] = message.text
        db.set_url(message.from_user.id, data['media'])
        await message.answer('Посилання успішно збережено', reply_markup=nav.mainMenu)
        await state.finish()

async def set_type_malling(message: Message): 
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='З медиа', callback_data='with_type'),InlineKeyboardButton(text='Немає медіа', callback_data='without_type'))
    await message.answer('Виберіть тип запланованой розсилки (з медіа або без)', reply_markup=keyboard)

async def handler_type_malling(call: CallbackQuery):
    
    call_data = call.data.split('_')
    await bot.answer_callback_query(call.id)
    await call.message.delete()
    if call_data[0] == 'with':
        db.set_type_malling_db(call_data[0], call.from_user.id)
        await bot.send_message(call.from_user.id, 'Тип розсилки змінено на "Розсилання з медіа"', reply_markup=nav.mainMenu)
    elif call_data[0] == 'without':
        db.set_type_malling_db(call_data[0], call.from_user.id)
        await  bot.send_message(call.from_user.id,'Тип розсилки змінено на "Розсилання без медіа"', reply_markup=nav.mainMenu)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(load_media,text='Посилання на медіа', state=None)
    dp.register_message_handler(handler_media, state=UrlLoader.url_media)
    dp.register_message_handler(set_type_malling, text='Тип розсилки')
    dp.register_callback_query_handler(handler_type_malling, Regexp('type'))
    # dp.register_message_handler(load_video,content_types=ContentType.VIDEO)