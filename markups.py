from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import config
config = config.token

from admins import bot
razdel = '🌀 Магазин 🌀'
# from db import Database
# from aiogram.utils.callback_data import CallbackData

# db = Database('user_db.db')
subMenu = InlineKeyboardMarkup(row_width=2)
btnYes = InlineKeyboardButton(text="Так", callback_data='btnYes')
btnNo = InlineKeyboardButton(text="Ні", callback_data='btnNo')

subMenu.add(btnYes, btnNo)

tryMenu = InlineKeyboardMarkup(row_width=2)
btnTry = InlineKeyboardButton(
    text="Попробовать еще раз", callback_data='btnTry')
btnCancel = InlineKeyboardButton(text="Відміна", callback_data='btnCancel')

tryMenu.add(btnTry, btnCancel)

cancelMenu = InlineKeyboardMarkup(row_width=1)
btnCancel2 = InlineKeyboardButton(text="Відміна", callback_data='btnCancel2')

cancelMenu.add(btnCancel2)

doneMenu = InlineKeyboardMarkup(row_width=2)
btnDone = InlineKeyboardButton(text="Готово", callback_data='btnDone')
btnCancel3 = InlineKeyboardButton(text="Відміна", callback_data='btnCancel3')

doneMenu.add(btnDone, btnCancel3)
keymain = (KeyboardButton('Керування функціями'))
key_back = (KeyboardButton('Головна сторінка'))

startpr_btn = (KeyboardButton('⏱Увімк бота'))
stoppr_btn = (KeyboardButton('🚫Вимк бота'))
post_btn = (KeyboardButton('Тарифи'))
pub_btn = (KeyboardButton('Керування автопостом'))
help_btn = (KeyboardButton('Допомога'))

Back_in = (KeyboardButton('Назад'))
newl_btn = (KeyboardButton('Новини'))

host_shop = (KeyboardButton('Замовити Хостинг'))
host_shop0 = (KeyboardButton('1 Місяць Оренди'))
host_shop3 = (KeyboardButton('3 Місяці Оренди'))
host_shop6 = (KeyboardButton('6 Місяців Оренди'))
host_shop12 = (KeyboardButton('12 Місяців Оренди'))

menu_in = (KeyboardButton('Замовити Рекламу'))
partners_btn = (KeyboardButton('1 Місяць'))
partners3_btn = (KeyboardButton('3 Місяці '))
partners6_btn = (KeyboardButton('6 Місяців'))
partners7_btn = (KeyboardButton('12 Місяців'))

grafic_btn = (KeyboardButton('Графік публікацій'))
FAQ_btn = (KeyboardButton('Інфо'))

toptext_btn = (KeyboardButton('Заголовок поста'))
middletext_btn = (KeyboardButton('Середина поста'))
bottomtext_btn = (KeyboardButton('Низ поста'))

addchanel_btn = (KeyboardButton('Додати канал'))
delchanels_btn = (KeyboardButton('Видалити канали'))
delchanel_btn = (KeyboardButton('Видалити 1 канал'))

addmoder_btn = (KeyboardButton('Додати админа'))
allmoders_btn = (KeyboardButton('Список адмінів'))
delmoder_btn = (KeyboardButton('Видалити админа'))

send_btn = (KeyboardButton('Надіслати пост'))
delete_btn = (KeyboardButton('Видалити пости'))
showtext_btn = (KeyboardButton('Показати пост'))
showchnl_btn = (KeyboardButton('Список каналів'))
loadMedia = (KeyboardButton('Посилання на медіа'))
typeMalling = (KeyboardButton('Тип розсилки ')) #Файл media.py

# создаём клавиатуру: Для Администратора бота
OSNMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
OSNMenu.add(keymain)                                        #Создаем клавиатуру: Керування функціями
OSNMenu.add(post_btn, help_btn, newl_btn)                   #Создаем клавиатуру: Тарифи/ Допомога/ Новости
OSNMenu.add(grafic_btn, FAQ_btn)                            #Создаем клавиатуру: График рассылки/Инфо
OSNMenu.add(menu_in)                                        #Создаем клавиатуру: Замовити Рекламу
OSNMenu.add(host_shop)                                      #Создаем клавиатуру: Замовити Хостинг
OSNMenu.add(pub_btn)                                        #Создаем клавиатуру: Интервал публикаций
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
mainMenu.add(key_back)                                       # создаём клавиатуру: Повернутися на головне меню
mainMenu.add(startpr_btn, stoppr_btn)                        # Создаем клавиатуру: Вкл авто-публ/выкл авто-публикации
mainMenu.add(toptext_btn, middletext_btn, bottomtext_btn)    # создаём клавиатуру: Заголовок/Середина/Низ
mainMenu.add(addchanel_btn, delchanels_btn, delchanel_btn)   #Добавить канал/Удалить каналы/Удалить один канал
mainMenu.add(addmoder_btn, allmoders_btn, delmoder_btn)      # создаём клавиатуру: Добавить модератора/Список модераторов/Удалить модератора
mainMenu.add(send_btn, delete_btn)                           # создаём клавиатуру: Отправить пост/Удалить посты
mainMenu.add(showtext_btn, showchnl_btn)                     # создаём клавиатуру: показать пост/список каналов
mainMenu.add(loadMedia, typeMalling)                         # создаём клавиатуру: Ссылка на медиа/Тип рассылки


# создаём клавиатуру: Для Модератора
moderMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
moderMenu.add(addchanel_btn, delchanels_btn) # создаём клавиатуру: Добавить канал и удалить канал
moderMenu.add(post_btn, help_btn, newl_btn) # создаём клавиатуру: Магазин
moderMenu.add(grafic_btn, FAQ_btn) #Создаем клавиатуру: График рассылки/Инфо
moderMenu.add(host_shop, menu_in)
# создаём клавиатуру: Для юзера
userMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
userMenu.add(post_btn, help_btn, FAQ_btn) # создаём клавиатуру: Тарифи/ Допомога/ Інфо
userMenu.add(grafic_btn, newl_btn, ) #Создаем клавиатуру: Купити таріф/График рассылки/ Новости
userMenu.add(menu_in, host_shop)  #Создаем клавиатуру: Купити таріф/

# создаём клавиатуру: Вибір тарифу Реклами
partnersMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
partnersMenu.add(partners_btn, partners3_btn) #Купить на місяць/купить на 3 місяця/
partnersMenu.add(partners6_btn, partners7_btn )
partnersMenu.add(Back_in) #Поверненя на головне меню

# создаём клавиатуру: Вибір тарифу Хастинга
host_shopMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
host_shopMenu.add(host_shop0, host_shop3) #Купить на місяць/купить на 3 місяця/
host_shopMenu.add(host_shop6, host_shop12 ) #Купить на 6 / 12 місяців
host_shopMenu.add(Back_in) #Поверненя на головне меню



async def genmarkup(list_data):  # передаём в функцию data
    markup = InlineKeyboardMarkup()  # создаём клавиатуру
    markup.insert_width = 1  # кол-во кнопок в строке
    for item in list_data:
        for i in item:
            chat_info = await bot.get_chat(i)
        # Создаём кнопки, i[1] - название, i[2] - каллбек дата
            markup.add(InlineKeyboardButton(f"💉 Видалити {chat_info['title']}", callback_data=f'del_{i}'))
    return markup

def accepting(type):
    markup = InlineKeyboardMarkup()  # создаём клавиатуру
    markup.add(InlineKeyboardButton(text='Так', callback_data=f'accept_{type}'), InlineKeyboardButton(text='Ні', callback_data=f'decline'))
    return markup