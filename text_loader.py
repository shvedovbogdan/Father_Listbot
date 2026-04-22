import asyncio

import aioschedule
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher.filters import Regexp
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode

import markups as nav
from admins import admin_id
from admins import bot, TOKEN
from db import Database
from test import generate_links

db = Database('user_db.db')


class TextLoader(StatesGroup):
    upper_text = State()
    middle_text = State()
    end_text = State()
    chanels_id = State()


# @dp.message_handler(commands='set_start', state=None)


async def add_upper_text(message: types.Message):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1:
            await TextLoader.upper_text.set()
            await message.answer('<b>Введіть верхню частину поста:</b>', reply_markup=nav.cancelMenu)


# @dp.message_handler(commands='set_links', state=TextLoader.upper_text, content_types=['text'])


async def load_upper_text(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1:
            async with state.proxy() as data:
                data['upper_text'] = message.text
                upper_text = generate_links(data['upper_text'])

                upper_text += ''.join('🌀━━━━━━━━━━━━━━━━━🌀')
            db.set_messageuper(message.from_user.id, upper_text)
            await message.answer(upper_text, parse_mode='HTML', disable_web_page_preview=True)
            await state.finish()

            # await TextLoader.next()


# @dp.message_handler(state=TextLoader.middle_text, content_types=['text'])
async def add_middle_text(message: types.Message):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1:
            await TextLoader.middle_text.set()
            await message.answer('<b>Введіть середину поста</b>', reply_markup=nav.cancelMenu)


async def load_middle_text(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1:
            async with state.proxy() as data:
                data['middle_text'] = message.text
                middle_text = generate_links(data['middle_text'])
                middle_text += ''.join('🌀━━━━━━━━━━━━━━━━━🌀')

            db.set_messagemiddle(message.from_user.id, middle_text)
            await message.answer(middle_text, parse_mode='HTML', disable_web_page_preview=True)
            await state.finish()

            # await TextLoader.next()


# @dp.message_handler(state=TextLoader.end_text, content_types=['text'])
async def add_end_text(message: types.Message):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1:
            await message.answer('<b> Введіть низ поста </b>', reply_markup=nav.cancelMenu)
            await TextLoader.end_text.set()


async def load_end_text(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1:
            async with state.proxy() as data:
                data['end_text'] = message.text
                bottom_text = generate_links(data['end_text'])
                # bottom_text += ''.join('🌀━━━━━━━━━━━━━━━━━🌀')
            db.set_messagebottom(message.from_user.id, bottom_text)
            await message.answer(bottom_text, parse_mode='HTML', disable_web_page_preview=True)
            await message.answer(db.get_messagepost(message.chat.id), parse_mode='HTML', disable_web_page_preview=True)
            await message.reply('Все збережено успішно')

            await state.finish()


async def get_db_text(message: types.Message):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is True:
            db.set_nickname(message.from_user.id, message.from_user.first_name)
            if db.admin_status(message.from_user.id) == 1:
                try:
                    await message.answer(                        #Текст для шапки бота
                        f"<a href='{db.get_url(message.from_user.id)}'>List Bot</a>\n{db.get_messagepost(message.chat.id)}",
                        parse_mode=ParseMode.HTML)
                    # await message.answer(db.get_messagepost(), disable_web_page_preview=True)
                except Exception as ex:
                    await message.answer(f'<u>Повідомлення порожнє</u> \n <code>{ex}</code>', parse_mode='HTML')
            elif db.admin_status(message.from_user.id) == 0 and message.from_user.id == admin_id:
                db.set_admin(message.from_user.id)
                await message.answer(str(db.get_messagepost(message.chat.id)))
            else:
                await message.answer('Ви не є ні адміністратором ні модератором каналу')


async def add_chanel_db(message: types.Message):
    if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1 or db.moder_status(
            message.from_user.id) == 1:
        db.set_nickname(message.from_user.id, message.from_user.first_name)
        try:
            await message.answer(
                '<b>➕ Для підключення каналу вам потрібно:\n\n'
                '1.Додати цього @Father_Listbot бота до себе в адміністратори, і дати йому такі дозволи:\n\n'
                '1.Редагування \n2.Публікації \n3.Видалення повідомлень. \n\n'
                '2. Коли дасте боту права: \n[ЯКЩО У ВАС ПУБЛІЧНИЙ КАНАЛ АБО ЧАТ] \n'
                'Напишіть сюди посилання на канал або чат у форматі @groupname або ID вашого каналу.\n\n'
                '[ЯКЩО У ВАС ПУБЛІЧНИЙ КАНАЛ АБО ЧАТ] </b> \n\n'
                '<i>Якщо у вас не виходить якісь з цих дій, то перешліть у бот</i> @getmyid_bot <i> будь-яке повідомлення з каналу або групи в якій має бути бот, '
                '@getmyid_bot даст id \n'
                '\nYour user ID: ІД Користувача'
                '\nCurrent chat ID: ІД відправника повідомлення'
                '\nForwarded from chat:- в поле ``-ІД Канала/Групи``.\n Після чого відправте його сюди. </i>',
                reply_markup=nav.cancelMenu)
            await TextLoader.chanels_id.set()
        except Exception as ex:
            await message.answer(f'Помилка {ex}')


chanels_to_db = []
error_channels_list = ''


async def load_chanel_db(message: types.Message, state: FSMContext):
    if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1 or db.moder_status(
            message.from_user.id) == 1:
        global chanels_to_db
        global error_channels_list
        async with state.proxy() as data:
            # data['chanels_id'] = message.forward_from_chat.id

            if message.forward_from_chat:
                if message.forward_from_chat['type'] == 'channel':
                    idshnik = message.forward_from_chat['id']
                    data['chanels_id'] = idshnik
                    chanels_review_to_db = data['chanels_id']
                    if str(chanels_review_to_db) in chanels_to_db:
                        await bot.send_message(message.from_user.id, 'Цей канал чи група вже є у списку.')
                    else:
                        try:
                            member = await bot.get_chat_member(chanels_review_to_db, TOKEN.split(":")[0])
                            # print(member)
                            is_administrator = '❌'
                            can_post = '❌'
                            can_edit = '❌'
                            can_del = '❌'
                            # and member['user']['id'] == TOKEN.split(":")[0]:
                            if member['status'] == 'administrator':
                                is_administrator = '✅'
                            if member['can_post_messages'] == True:
                                can_post = '✅'
                            if member['can_edit_messages'] == True:
                                can_edit = '✅'
                            if member['can_delete_messages'] == True:
                                can_del = '✅'
                            if member['can_post_messages'] == False:
                                can_post = '❌'
                            if member['can_edit_messages'] == False:
                                can_edit = '❌'
                            if member['can_delete_messages'] == False:
                                can_del = '❌'
                            if not member['status'] == 'administrator':
                                is_administrator = '❌'
                            if is_administrator == '✅' and can_post == '✅' and can_edit == '✅' and can_del == '✅':
                                chanels_to_db.append(chanels_review_to_db)
                                # chanels_to_db.append(chanels_review_to_db)
                                await message.answer(
                                    f'{chanels_review_to_db} успішно доданий \nЯкщо хочете додати інший ще один чат або канал, продовжуйте вводити '
                                    f'ID або @username каналу або чату або надсилати повідомлення.\nДля завершення натисніть Готово або Скасувати, '
                                    f'якщо хочете скасувати додавання каналів',
                                    reply_markup=nav.doneMenu)

                            if is_administrator == '❌' or can_post == '❌' or can_edit == '❌' or can_del == '❌':
                                await bot.send_message(message.from_user.id,
                                                       f'Ви наділили бота в {chanels_review_to_db} не всіма правами: \nбот є адміном - {is_administrator} \nПублікація повідомлень - {can_post} \nРедагування публікацій - {can_edit} \nВидалення публікацій - {can_del}',
                                                       reply_markup=nav.tryMenu)
                                # error_channels_list += ''.join(i) + ' '

                        except Exception as ex:
                            await bot.send_message(message.from_user.id,
                                                   f'<b>Канал або чат {chanels_to_db} не розпізнаний. Надішліть @username або ID каналу (чату) одним словом.'
                                                   f' Якщо ви додаєте приватний канал - спробуйте переслати будь-яке повідомлення з нього прямо сюди,'
                                                   f' а якщо хочете додати чат - видаліть бота з адміністраторів чату і додайте його ще раз з облікового запису адміністратора чату</b> \n<code>{ex}</code>',
                                                   reply_markup=nav.cancelMenu)

            elif message.forward_from_chat:
                if message.forward_from_chat['type'] == 'supergroup':
                    idshnik = message.forward_from_chat['id']
                    data['chanels_id'] = idshnik
                    chanels_review_to_db = data['chanels_id']
                    if chanels_review_to_db in chanels_to_db:
                        await bot.send_message(message.from_user.id, 'Цей канал чи група вже є у списку.')
                    else:
                        try:
                            member = await bot.get_chat_member(chanels_review_to_db, TOKEN.split(":")[0])

                            is_administrator = '❌'
                            can_mang_chat = '❌'
                            can_del = '❌'

                            if member['status'] == 'administrator':
                                is_administrator = '✅'
                            if member['can_manage_chat'] == True:
                                can_mang_chat = '✅'
                            if member['can_delete_messages'] == True:
                                can_del = '✅'
                            if member['can_manage_chat'] == False:
                                can_mang_chat = '❌'
                            if member['can_delete_messages'] == False:
                                can_del = '❌'
                            if not member['status'] == 'administrator':
                                is_administrator = '❌'
                            if is_administrator == '✅' and can_mang_chat == '✅' and can_del == '✅':
                                chanels_to_db.append(chanels_review_to_db)

                                await message.answer(
                                    f'{chanels_review_to_db} успішно доданий \nЯкщо хочете додати інший ще один чат або канал, продовжуйте вводити '
                                    f'\ID или @username каналу або чату або надсилати повідомлення.\nЩоб завершити, натисніть Готово або Скасувати, якщо хочете скасувати додавання каналів',
                                    reply_markup=nav.doneMenu)

                            if is_administrator == '❌' or can_mang_chat == '❌' or can_del == '❌':
                                await bot.send_message(message.from_user.id,
                                                       f'Вы наделили бота в {chanels_review_to_db} не всіма правами: \nБот є адміном - {is_administrator} \nПублікація повідомлень - {can_mang_chat}\nВидалення публікацій - {can_del}',
                                                       reply_markup=nav.tryMenu)
                                # error_channels_list += ''.join(i) + ' '

                        except Exception as ex:
                            await bot.send_message(message.from_user.id,
                                                   f'<b>Канал или чат {chanels_to_db}не розпізнаний. Надішліть @username або ID каналу (чату) одним словом.'
                                                   f'Якщо ви додаєте приватний канал, спробуйте переслати будь-яке повідомлення з нього прямо сюди. '
                                                   f'а якщо хочете додати чат - видаліть бота з адміністраторів чату і додайте його ще раз з облікового запису адміністратора чату</b> \n<code>{ex}</code>',
                                                   reply_markup=nav.cancelMenu)

            else:
                data['chanels_id'] = message.text
                chanels_review_to_db = str(data['chanels_id']).split()
                for i in chanels_review_to_db:
                    if i in chanels_to_db:
                        await bot.send_message(message.from_user.id, 'Цей канал чи група вже є у списку.')
                    else:
                        try:
                            type_chat = await bot.get_chat(i)
                            if type_chat['type'] == 'supergroup':
                                # try:
                                member = await bot.get_chat_member(i, TOKEN.split(":")[0])
                                print(member)
                                is_administrator = '❌'
                                can_mang_chat = '❌'
                                can_del = '❌'

                                if member['status'] == 'administrator':
                                    is_administrator = '✅'
                                if member['can_manage_chat'] is True:
                                    can_mang_chat = '✅'
                                if member['can_delete_messages'] is True:
                                    can_del = '✅'
                                if member['can_manage_chat'] is False:
                                    can_mang_chat = '❌'
                                if member['can_delete_messages'] is False:
                                    can_del = '❌'
                                if not member['status'] == 'administrator':
                                    is_administrator = '❌'
                                if is_administrator == '✅' and can_mang_chat == '✅' and can_del == '✅':
                                    chanels_to_db.append(i)
                                    # chanels_to_db.append(chanels_review_to_db)
                                    await message.answer(f'{i} Успешно добавлен')

                                if is_administrator == '❌' or can_mang_chat == '❌' or can_del == '❌':
                                    await bot.send_message(message.from_user.id,
                                                           f'Вы наделили бота в {chanels_review_to_db} не всіма правами: \nБот є адміном - {is_administrator} \nПублікація повідомлень - {can_mang_chat}\nВидалення публікацій - {can_del}',
                                                           reply_markup=nav.tryMenu)
                                    error_channels_list += ''.join(i) + ' '
                            

                            else:
                                try:
                                    member = await bot.get_chat_member(i, TOKEN.split(":")[0])
                                    is_administrator = '❌'
                                    can_post = '❌'
                                    can_edit = '❌'
                                    can_del = '❌'
                                    if member['status'] == 'administrator':
                                        is_administrator = '✅'
                                    if member['can_post_messages'] is True:
                                        can_post = '✅'
                                    if member['can_edit_messages'] is True:
                                        can_edit = '✅'
                                    if member['can_delete_messages'] is True:
                                        can_del = '✅'
                                    if member['can_post_messages'] is False:
                                        can_post = '❌'
                                    if member['can_edit_messages'] is False:
                                        can_edit = '❌'
                                    if member['can_delete_messages'] is False:
                                        can_del = '❌'
                                    if not member['status'] == 'administrator':
                                        is_administrator = '❌'
                                    if is_administrator == '✅' and can_post == '✅' and can_edit == '✅' and can_del == '✅':
                                        chanels_to_db.append(i)
                                        # chanels_to_db.append(chanels_review_to_db)
                                        await message.answer(f'{i} успішно доданий')
                                    if is_administrator == '❌' or can_post == '❌' or can_edit == '❌' or can_del == '❌':
                                        await bot.send_message(message.from_user.id,
                                                               f'Ви наділили бота в {i} не всіма правами: \nБот є адміном - {is_administrator} \nПублікація повідомлень - {can_post} \nРедагування публікацій - {can_edit} \nВидалення публікацій - {can_del}',
                                                               reply_markup=nav.tryMenu)
                                        error_channels_list += ''.join(i) + ' '
                                    is_administrator = '❌'
                                    can_post = '❌'
                                    can_edit = '❌'
                                    can_del = '❌'

                                except Exception as ex:
                                    await bot.send_message(message.from_user.id,
                                                           f'<b>Канал або чат {i} не розпізнаний.</b> Надішліть @username або ID каналу (чату) одним словом.'
                                                           f' <i>Якщо ви додаєте приватний канал, спробуйте переслати будь-яке повідомлення з нього прямо сюди,'
                                                           f' а якщо хочете додати чат - видаліть бота з адміністраторів чату і додайте його ще раз з облікового запису адміністратора чату</i> \n<code>{ex}</code>',
                                                           reply_markup=nav.cancelMenu)

                        except Exception as ex:
                            await bot.send_message(message.from_user.id,
                                                   f'<b>Канал або чат {i} не розпізнаний.</b> Надішліть @username або ID каналу (чату) одним словом.'
                                                   f' <i>Якщо ви додаєте приватний канал, спробуйте переслати будь-яке повідомлення з нього прямо сюди,'
                                                   f' а якщо хочете додати чат - видаліть бота з адміністраторів чату і додайте його ще раз з облікового запису адміністратора чату</i> \n<code>{ex}</code>',
                                                   reply_markup=nav.cancelMenu)
                await message.answer(
                    'Якщо хочете додати інший інший чат або канал, продовжуйте вводити ID або @username каналу або чату або надсилати повідомлення.\nЩоб завершити, натисніть Готово або Скасувати, якщо хочете скасувати додавання каналів',
                    reply_markup=nav.doneMenu)
        # except Exception as ex:
        #     await bot.send_message(message.from_user.id, f'<b>Произошла ошибка добавления бота в БД.</b> \n<code>{ex}</code>', reply_markup=nav.btnCancel )

        ##### НАПОМИНАЛКА #####


async def trying(message: types.Message, state: FSMContext):
    if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1 or db.moder_status(
            message.from_user.id) == 1:
        global chanels_to_db
        global error_channels_list
        try:

            for i in error_channels_list.split():
                if i in chanels_to_db:
                    await bot.send_message(message.from_user.id, 'Цей канал чи група вже є у списку.')
                else:
                    type_chat = await bot.get_chat(i)
                    if type_chat['type'] == 'supergroup':
                        try:
                            member = await bot.get_chat_member(i, TOKEN.split(":")[0])
                            is_administrator = '❌'
                            can_mang_chat = '❌'
                            can_del = '❌'
                            if member['status'] == 'administrator':
                                is_administrator = '✅'
                            if member['can_manage_chat'] == True:
                                can_mang_chat = '✅'
                            if member['can_delete_messages'] == True:
                                can_del = '✅'
                            if member['can_manage_chat'] == False:
                                can_mang_chat = '❌'
                            if member['can_delete_messages'] == False:
                                can_del = '❌'
                            if not member['status'] == 'administrator':
                                is_administrator = '❌'
                            if is_administrator == '✅' and can_mang_chat == '✅' and can_del == '✅':
                                chanels_to_db.append(i)
                                # chanels_to_db.append(chanels_review_to_db)
                                await bot.send_message(message.from_user.id,
                                                       f'{i} успішно доданий \nякщо хочете додати інший ще один чат або канал, продовжуйте вводити ID або @username каналу або чату або надсилати повідомлення.\nЩоб завершити, натисніть Готово або Скасувати, якщо хочете скасувати додавання каналів',
                                                       reply_markup=nav.doneMenu)

                            if is_administrator == '❌' or can_mang_chat == '❌' or can_del == '❌':
                                await bot.send_message(message.from_user.id,
                                                       f'Ви наділили бота в {i} не всіма правами: \nБот є адміном - {is_administrator} \nПублікація повідомлень - {can_mang_chat}\nВидалення публікацій - {can_del}',
                                                       reply_markup=nav.tryMenu)
                        except Exception as ex:
                            await bot.send_message(message.from_user.id,
                                                   f'<b>Канал або чат {i} не розпізнаний. Надішліть @username або ID каналу (чату) одним словом.'
                                                   f' Якщо ви додаєте приватний канал, спробуйте переслати будь-яке повідомлення з нього прямо сюди,'
                                                   f' а якщо хочете додати чат - видаліть бота з адміністраторів чату і додайте його ще раз з облікового запису адміністратора чату</b> \n<code>{ex}</code>',
                                                   reply_markup=nav.cancelMenu)
                    else:
                        try:
                            member = await bot.get_chat_member(i, TOKEN.split(":")[0])
                            is_administrator = '❌'
                            can_post = '❌'
                            can_edit = '❌'
                            can_del = '❌'
                            # and member['user']['id'] == TOKEN.split(":")[0]:
                            if member['status'] == 'administrator':
                                is_administrator = '✅'
                            if member['can_post_messages'] == True:
                                can_post = '✅'
                            if member['can_edit_messages'] == True:
                                can_edit = '✅'
                            if member['can_delete_messages'] == True:
                                can_del = '✅'
                            if member['can_post_messages'] == False:
                                can_post = '❌'
                            if member['can_edit_messages'] == False:
                                can_edit = '❌'
                            if member['can_delete_messages'] == False:
                                can_del = '❌'
                            if not member['status'] == 'administrator':
                                is_administrator = '❌'
                            if is_administrator == '✅' and can_post == '✅' and can_edit == '✅' and can_del == '✅':
                                chanels_to_db.append(i)
                                # chanels_to_db.append(i)
                                await bot.send_message(message.from_user.id,
                                                       f'{i} успішно додані \nЯкщо хочете додати інший інший чат або канал, продовжуйте вводити ID або @username каналу або чату або надсилати повідомлення.\nЩоб завершити, натисніть Готово або Скасувати, якщо хочете скасувати додавання каналів',
                                                       reply_markup=nav.doneMenu)
                            if is_administrator == '❌' or can_post == '❌' or can_edit == '❌' or can_del == '❌':
                                await bot.send_message(message.from_user.id,
                                                       f'Ви наділили бота в {i} не всіма правами: \nБот є адміном - {is_administrator} \nПублікація повідомлень - {can_post} \nРедагування публікацій - {can_edit} \nВидалення публікацій - {can_del}',
                                                       reply_markup=nav.tryMenu)

                        except Exception as ex:
                            await bot.send_message(message.from_user.id,
                                                   f'<b>Сталася помилка додавання бота до БД. Можливо, бот не доданий до каналу або чату як адміністратор.</b> \n<code>{ex}</code>',
                                                   reply_markup=nav.btnCancel)
        except Exception as ex:
            await bot.send_message(message.from_user.id,
                                   f'<b>Сталася помилка додавання бота до БД. Можливо, бот не доданий до каналу або чату як адміністратор.</b> \n<code>{ex}</code>',
                                   reply_markup=nav.btnCancel)


async def done(call: types.CallbackQuery, state: FSMContext):
    global chanels_to_db
    await call.message.delete()
    already_in_db = db.get_chanel_list(call.message.chat.id)
    print(already_in_db)

    for i in chanels_to_db:
        if i in already_in_db:
            continue
        else:
            db.add_chanel_list(i,call.message.chat.id)
    await state.finish()
    await bot.send_message(call.message.chat.id, 'Канали додані до БД')
    chanels_to_db = []


async def cancel3(message: types.Message, state: FSMContext):
    global chanels_to_db
    await state.finish()
    chanels_to_db = []
    await bot.send_message(message.from_user.id, 'Скасування додавання каналів.', reply_markup=nav.mainMenu)


async def delete_chanel_from_db(message: types.Message):
    if db.user_exists(message.from_user.id) is True:
        # if db.moder_status(message.from_user.id) == 1:
        #     db.del_chanel_list(message.from_user.id)
        #     await bot.send_message(message.from_user.id, f'Каналы удалены \n{start_message2}')
        if db.admin_status(message.from_user.id) == 1:
            db.del_all_channels()
            await bot.send_message(message.from_user.id, f'Усі канали видалені', reply_markup=nav.mainMenu)


async def delete_chanel(message: types.Message):
    if db.admin_status(message.from_user.id) == 1:

        list_data = db.get_chanel_list(message.chat.id)

                # await bot.send_message(message.from_user.id, f'{chat_info["title"]}',
                #                            reply_markup=nav.genmarkup(item,chat_info["title"]))
        await bot.send_message(message.from_user.id, "Виберіть канал для видалення", reply_markup=await nav.genmarkup(list_data))

# @dp.callback_query_handler(lambda call:True)


async def kb_delete_chanel_answer(callback_query: types.CallbackQuery):
    if 'del' in callback_query.data.split('_')[0]:
        await bot.answer_callback_query(callback_query.id)
        choosen_chanel = str(callback_query.data.split('_')[1])
        db.del_current_channel(choosen_chanel)
        chanel_title = await bot.get_chat(choosen_chanel)
        await bot.send_message(callback_query.from_user.id, f'Канал <b>{chanel_title["title"]}</b> видалено')


async def help_menu(callback_query: types.CallbackQuery, state: FSMContext):
    if db.admin_status(admin_id) == 1:

        await state.finish()
        try:
            await callback_query.message.delete()
            await bot.send_message(admin_id, 'Меню', reply_markup=nav.mainMenu)
        except Exception as ex:
            await bot.send_message(admin_id, f'<b>Виникла помилка</b> \n<code>{ex}</code>')


async def chanels_check(message: types.message):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1:
            channels_list = db.get_all_channels()
            chat_name_list = ''
            for i in channels_list:
                for item in i:
                    try:
                        if i[0] == '@':
                            chat_name_list += ''.join(item) + '\n'
                        else:
                            chat_info = await bot.get_chat(item)
                            if chat_info['title'] in chat_name_list:
                                continue
                            else:
                                chat_name_list += ''.join(
                                    chat_info['title']) + '\n'

                    except Exception as ex:
                        await bot.send_message(message.from_user.id, f'Розсилка буде такими каналами \n{chat_name_list}')
                        await message.answer(f'<b>Помилка</b> \n<code>{ex}</code> --> <i>{item}</i>', parse_mode='HTML')
            await bot.send_message(message.from_user.id,
                                   f'Канали, які є в базі даних для розсилки\n{chat_name_list}')

async def chanels_malling_info(message: types.Message):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1:
            channels_list = db.get_chanel_list(message.chat.id)
            chat_name_list = ''
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(text='Медиа', callback_data='add_media'),
                types.InlineKeyboardButton(text='Нічого не додавати', callback_data='add_nothing'))

            for item in channels_list:
                for i in item:
                    try:
                        chat_info = await bot.get_chat(i)
                        if chat_info['title'] in chat_name_list:
                            continue
                        else:
                            chat_name_list += ''.join(
                                chat_info['title']) + '\n'

                    # await bot.send_message(message.from_user.id, f'Рассылка будет по таким каналам \n{chat_name_list} \nЕсли вы согласны нажмите "Да". Если не согласны нажмите "Нет"', reply_markup=nav.subMenu)
                    except Exception as ex:
                        await message.answer(f'<b>Помилка</b> \n<code>{ex}</code> --> <i>{i}</i>', )
            await bot.send_message(message.from_user.id,
                                   f'Розсилка буде такими каналами \n{chat_name_list} \nБажаєте додати фото чи відео',
                                   reply_markup=keyboard)

async def video_photo_handler(call: types.CallbackQuery):
    call_data = call.data.split('_')
    await bot.answer_callback_query(call.id)
    await call.message.delete()
    channels_list = db.get_chanel_list(call.message.chat.id)
    chat_name_list = ''

    for item in channels_list:
        for i in item:
            chat_info = await bot.get_chat(i)
            if chat_info['title'] in chat_name_list:
                continue
            else:
                chat_name_list += ''.join(
                    chat_info['title']) + '\n'
    if call_data[1] == 'media':
        await bot.send_message(call.from_user.id,
                               f'Розсилка буде такими каналами \n{chat_name_list} \nЯкщо ви згодні, натисніть "Так". Якщо не згодні, натисніть "Ні"',
                               reply_markup=nav.accepting(call_data[1]))
    elif call_data[1] == 'nothing':
        await bot.send_message(call.from_user.id,
                               f'Розсилка буде такими каналами \n{chat_name_list} \nЯкщо ви згодні, натисніть "Так". Якщо не згодні, натисніть "Ні"',
                               reply_markup=nav.accepting(call_data[1]))


# отправка по графику

async def periodic(user_id):
    print(user_id)
    channels_list = db.get_all_user_channels(user_id)
    print(channels_list)
    for el2 in channels_list:
        for i in el2:
            channels_id = await bot.get_chat(i)

            try:
                if db.get_type_malling_db(admin_id) == 'with':
                    text = db.get_messagepost(user_id)
                    msg = await bot.send_message(i,
                                                 f"<a href='{db.get_url(admin_id)}'>⚜️List Bot⚜️</a>\n{text}",
                                                 parse_mode=ParseMode.HTML)
                else:
                    msg = await bot.send_message(i, db.get_messagepost(user_id), disable_web_page_preview=True)
                # msg = await bot.send_message(el2, db.get_messagepost(), disable_web_page_preview=True)
                await bot.pin_chat_message(i, msg.message_id, disable_notification=True)
                db.set_message_chat_id(msg.message_id, i)
            except Exception as ex2:
                await bot.send_message(admin_id,
                                       f"У запланованій розсилці сталася помилка <code>{ex2}</code> \nКанал {i} - {channels_id['title']}. \nПости не надіслані.")


async def scheduler():
    # temp = aioschedule.every(30).seconds.do(periodic)

    try:
        for i in db.get_active_user_id():
            print(i)
            monday = aioschedule.every().monday.at('10:00').do(periodic,i[0])        #Понедельник
            tuesday = aioschedule.every().tuesday.at('10:00').do(periodic,i[0])      #Вторник
            wednesday = aioschedule.every().wednesday.at('10:00').do(periodic,i[0])  #Среда
            thursday = aioschedule.every().thursday.at('10:00').do(periodic,i[0])    #Четверг
            friday = aioschedule.every().friday.at('10:00').do(periodic,i[0])        #Пятница
            saturday = aioschedule.every().saturday.at('10:00').do(periodic,i[0])    #Субота
            sunday = aioschedule.every().sunday.at('14:00').do(periodic,i[0])        #Воскресенье
    except Exception as ex:
        await bot.send_message(admin_id, f'Помилка у надсиланні запланованого повідомлення \n<code>{ex}</code>')
    try:
        aioschedule.every().day.at('22:00').do(deleting)                             #Удаление
    except Exception as ex1:
        await bot.send_message(admin_id, f'Помилка у видаленні повідомлень \n<code>{ex1}</code>')
    if db.get_status_malling() == 1:
        print('[INFO] Розсилка запланована')
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        if db.get_status_malling() == 0:
            aioschedule.cancel_job(monday)
            aioschedule.cancel_job(tuesday)
            aioschedule.cancel_job(wednesday)
            aioschedule.cancel_job(thursday)
            aioschedule.cancel_job(friday)
            aioschedule.cancel_job(saturday)
            aioschedule.cancel_job(sunday)
            return
        else:
            continue


async def cencel_scheduler(message: types.Message):
    db.set_status_malling_0()
    await bot.send_message(message.from_user.id,
                           'Розсилка зупинена. Повідомлення видалятися після закінчення 24 годин, після відправки',
                           reply_markup=nav.mainMenu)


async def accepting(call: types.CallbackQuery):
    await call.message.delete()
    call_data = call.data.split('_')
    db.set_status_malling_1()
    channels_for_posting = []

    channels_list = db.get_all_user_channels(call.message.chat.id)


    for i in channels_list:

        for item in i:


            try:
                channels_id = await bot.get_chat(item)
                members = await bot.get_chat_administrators(item)
                if call_data[1] == 'media':
                    text = db.get_messagepost(call.message.chat.id)
                    msg = await bot.send_message(item,
                                                 f"<a href='{db.get_url(call.message.chat.id)}'>⚜️ List Bot⚜️</a>\n{text}",
                                                 parse_mode=ParseMode.HTML)
                else:
                    msg = await bot.send_message(item, db.get_messagepost(call.message.chat.id), disable_web_page_preview=True)

                    # await bot.edit_message_text(chat_id=el2, message_id=msg['message_id'],text=f"[snn](https://i.imgur.com/I43vHR4.jpeg)", parse_mode=ParseMode.MARKDOWN_V2)
                db.set_message_chat_id(msg.message_id, item)
                await bot.pin_chat_message(item, msg.message_id, disable_notification=True)
            except Exception as ex1:
                if str(ex1) == 'Need administrator rights in the channel chat':
                    for items in members:
                        if items['status'] == 'creator':
                            if db.user_exists(items['user']['id']) == True:
                                await bot.send_message(items['user']['id'],
                                                       f"Ви не наділили бота правами для розсилки. <code>{ex1}</code> \nКанал {i} - {channels_id['title']}. \nПублікація в канал не надіслано.")
                    await bot.send_message(admin_id,
                                           f"У запланованій розсилці сталася помилка <code>{ex1}</code> \nКанал {i} - {channels_id['title']}. \nПост не відправлений.")
                else:
                    await bot.send_message(admin_id,
                                           f"У запланованій розсилці сталася помилка <code>{ex1}</code> \nКанал {i} - {channels_id['title']}. \nПост не відправлений.")




    # await scheduler()
    channels_for_posting = []


async def deleting():
    try:
        message_id_list = db.get_message_id()
        if message_id_list == []:
            await bot.send_message(admin_id, 'Видаляти нічого')
        else:
            for msges in message_id_list:
                for el in msges:
                    chat_id_list = db.get_chat_id(el)
                    for i in chat_id_list:
                        for item in i:

                            try:
                                chat_info = await bot.get_chat(item)
                                await bot.delete_message(item, el)
                            except Exception as ex2:
                                await bot.send_message(admin_id,
                                                       f'Помилка видалення повідомлення у каналі <code>{ex2}</code> \nКанал:\n{item}')
            await bot.send_message(admin_id, 'Розсилка зупинена. Всі повідомлення видалено')
            db.clean_db()
    except Exception as ex:
        await bot.send_message(admin_id,
                               f'Помилка видалення повідомлення у каналі <code>{ex}</code>')


async def prbot_delete(message: types.Message):
    try:
        db.set_status_malling_0()
        await deleting()

    except Exception as ex:
        await bot.send_message(admin_id, f'Помилка видалення повідомлення{ex}')


async def deccepting(call: types.CallbackQuery):
    if db.user_exists(call.message.chat.id) is True and db.admin_status(call.message.chat.id) == 1:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        try:
            db.set_status_malling_0()
            await bot.send_message(call.message.chat.id, f"<b>Розсилання скасовано</b>", reply_markup=nav.mainMenu)
        except Exception as ex:
            await call.message.answer(f'<b>Помилка</b> \n<code>{ex}</code>')


# async def stop_chanels_malling(message: types.Message):
#     if message.chat.type == 'private':
#         if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1 or db.moder_status(message.from_user.id) == 1:
#             db.set_status_malling_0()
#             await bot.send_message(message.from_user.id, 'Розсилка зупинена')


async def start_chanels_malling(message: types.Message):
    global chatid_for_delete_msg
    global msg_id
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is True and db.admin_status(message.from_user.id) == 1:
            if db.get_status_malling() == 1:
                await bot.send_message(message.chat.id,
                                       f'Розсилка вже призначена. Щоб скасувати призначення розсилки напишіть /stop_pr')
            elif db.get_status_malling() == 0:
                try:
                    chat_name_list = ''
                    channels_list = db.get_all_channels()
                    db.set_status_malling_1()


                    for item in channels_list:
                        for i in item:
                            chat_info = await bot.get_chat(i)
                            if chat_info['title'] in chat_name_list:
                                continue
                            else:
                                chat_name_list += ''.join(
                                    chat_info['title'] + '\n')

                    await bot.send_message(message.chat.id,
                                           f'Розсилка призначена. Канали: \n{chat_name_list}\nЩоб скасувати призначення розсилки, напишіть /stop_pr')

                    await scheduler()

                except Exception as ex:
                    await message.answer(f'<b>Помилка</b> \n<code>{ex}</code>')



def register_hendlers(dp: Dispatcher):
    dp.register_message_handler(
        add_upper_text, content_types=['text'], text='Заголовок поста', state=None)  #Готово
    dp.register_message_handler(
        load_upper_text, state=TextLoader.upper_text, content_types=['text'])
    dp.register_message_handler(
        add_middle_text, content_types=['text'], text='Середина поста', state=None, )  #Готово
    dp.register_message_handler(
        load_middle_text, state=TextLoader.middle_text, content_types=['text'])
    dp.register_message_handler(
        add_end_text, content_types=['text'], text='Низ поста', state=None, ) #Готово
    dp.register_message_handler(
        load_end_text, state=TextLoader.end_text, content_types=['text'])
    dp.register_message_handler(get_db_text, content_types=[
        'text'], text='Показати пост')                                     #Готово
    dp.register_message_handler(add_chanel_db, ChatTypeFilter(
        chat_type=types.ChatType.PRIVATE), content_types=['text'], text='Додати канал', state=None)    #Готово
    dp.register_message_handler(
        delete_chanel_from_db, content_types=['text'], text='Видалити канали')             #Готово
    dp.register_message_handler(delete_chanel, content_types=[
        'text'], text='Видалити 1 канал')                                                  #Готово
    dp.register_message_handler(load_chanel_db, ChatTypeFilter(
        chat_type=types.ChatType.PRIVATE), state=TextLoader.chanels_id, content_types=['text'])
    dp.register_message_handler(chanels_check, content_types=[
        'text'], text='Список каналів')                                            #Готово
    dp.register_callback_query_handler(
        kb_delete_chanel_answer, lambda call: call.data.split('_')[0] == 'del')
    dp.register_callback_query_handler(accepting, Regexp('accept'))
    dp.register_callback_query_handler(deccepting, Regexp('decline'))
    dp.register_callback_query_handler(video_photo_handler, Regexp('add'))
    dp.register_callback_query_handler(trying, ChatTypeFilter(
        chat_type=types.ChatType.PRIVATE), text='btnTry', state=TextLoader.chanels_id)
    dp.register_callback_query_handler(
        done, text='btnDone', state=TextLoader.chanels_id)
    dp.register_callback_query_handler(
        cancel3, text=['btnCancel3', 'btnCancel'], state=TextLoader.chanels_id)
    dp.register_callback_query_handler(
        help_menu, text='btnCancel2', state=TextLoader)
    dp.register_message_handler(chanels_malling_info, content_types=[
        'text'], text='Надіслати пост')                                        #Готово
    dp.register_message_handler(start_chanels_malling, content_types=[
        'text'], text='⏱Увімк бота')                                        #Готово
    # dp.register_message_handler(sending)
    # dp.register_message_handler(accepting, commands=['prbot_send'])
    dp.register_message_handler(cencel_scheduler, content_types=[
        'text'], text='🚫Вимк бота')                                     #Готово
    dp.register_message_handler(cencel_scheduler, commands=['stop_pr'])
    dp.register_message_handler(prbot_delete, content_types=[
        'text'], text='Видалити пости')                                 #Готово
