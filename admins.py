import config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from db import Database


class AdminHendlers(StatesGroup):
    new_moder = State()
    del_moder = State()
    waiting_for_Task = State()
# Добавить модера через фсм


db = Database('user_db.db')

TOKEN = config.token
admin_id = config.admin_id


bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


# if "," in get_id:
#     get_id = get_id.split(",")
#     for a in get_id:
#         ADMIN_ID.append(str(a))
# else:
#     try:
#         ADMIN_ID = [str(get_id)]
#     except ValueError:
#         ADMIN_ID = [0]
#         print("Не указан Admin_ID")


# def is_admin(user_id):
#     """
#     Проверка юзера на админа

#     :param user_id: id юзера
#     :return: true - юзер админ, false - нет
#     """
#     return str(user_id) in ADMIN_ID


# @dp.message_handler(IDFilter(chat_id=ADMIN_ID),commands=['add_moder'])
async def new_moder_set(message: types.Message):
    if message.chat.type == 'private':
        if (db.admin_status(message.from_user.id)) == 1:
            await AdminHendlers.new_moder.set()
            await message.answer('<b>Введите id для добавления модератора</b>', parse_mode="HTML")


# @dp.message_handler(IDFilter(chat_id=ADMIN_ID), state=AdminHendlers.new_moder)
async def new_moder(message: types.Message, state=FSMContext):
    if message.chat.type == 'private':
        async with state.proxy() as data:
            if message.text.isdigit():
                data['new_moder'] = message.text
                new_admin = (data['new_moder'])
                if db.user_exists(new_admin) is True:
                    db.set_moder(new_admin)
                    await message.answer('<b>Модератор успешно добавлен</b>')
                else:
                    await message.answer(f'<b>Такого челоека скорее всего нет в Базе Данных.</b> \n\n<i>Проверьте написанный ID {new_admin}</i>')
            else:
                await message.answer('<b>Не правильный формат ID</b>')
            await state.finish()

buttons_list = []


async def del_moder_list(message: types.Message):
    if message.chat.type == 'private':
        if db.admin_status(message.from_user.id) == 1:
            await message.answer('<b>Виберіть модератора, якого хочете видалити</b>')

            moder_list = ''
            temp_moder_list = []
            temp_moder_id_list = []
            global buttons_list
            buttons_list2 = []
            try:
                for i in db.get_moders():
                    for el in i:
                        temp_moder_id_list.append(el)
                        for elements in db.get_nickname(el):
                            for items in elements:
                                temp_moder_list.append(items)

                for nick, id_list in zip(temp_moder_list, temp_moder_id_list):
                    buttons_list.append([InlineKeyboardButton(
                        text=f'Видалити - {nick}', callback_data=id_list)])
                    buttons_list2.append([InlineKeyboardButton(
                        text=f'Видалити - {nick}', callback_data=id_list)])
                    keyboard_inline_buttons = InlineKeyboardMarkup(
                        inline_keyboard=buttons_list2, row_width=1)
                    await bot.send_message(message.from_user.id, f'{nick} - <code>{id_list}</code>', reply_markup=keyboard_inline_buttons)
                    buttons_list2 = []
                await bot.send_message(message.from_user.id, '[BETA VERSION] \nДля видалення модера напишіть /del *id_модератора* \n[BETA VERSION]')
            except Exception as ex:
                print(ex)


async def deleting(message: types.Message):
    moder_id = message.text[4:]
    db.del_moder(moder_id)
    await bot.send_message(message.from_user.id, 'Модератора видалено')


async def del_moder(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await AdminHendlers.waiting_for_Task.set()
    global executor
    executor = callback_query.data
    print(callback_query.data)
    await bot.send_message(callback_query.from_user.id, 'Ви обрали ім*я ->')


async def all_moders(message: types.Message):
    if message.chat.type == 'private':
        moder_list = db.get_moder_list()
        print(moder_list)
        moders_str = ''
        for i in moder_list:
            moders_str += ''.join(f'🆔{str(i[1])}  ||{i[0]}||\n')
        print(moders_str)
        await bot.send_message(message.from_user.id, f'Усі модератори: \n\n{moders_str}', parse_mode='MarkdownV2')


def register_hendlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        new_moder_set, content_types=['text'], text='Додати админа', state=None)
    dp.register_message_handler(new_moder, state=AdminHendlers.new_moder)
    dp.register_message_handler(all_moders, content_types=[
                                'text'], text='Список адмінів')
    dp.register_message_handler(del_moder_list, content_types=[
                                'text'], text='Видалити админа')
    dp.register_callback_query_handler(
        del_moder, text=buttons_list, state=None)
    dp.register_message_handler(deleting, commands='del')
