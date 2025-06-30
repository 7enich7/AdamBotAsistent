from NewBotAs.BOTIK import summ_game_list
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from os import getenv



isTake = getenv('MONITOR_SECOND') == '1'


but_back = KeyboardButton(text='Назад')
but_no = KeyboardButton(text='Нет')


but_game = KeyboardButton(text='Игры')
but_func = KeyboardButton(text='Функции')

markup_app = ReplyKeyboardMarkup(keyboard=[[but_func],
                                           [but_game]],
                                 resize_keyboard=True)



def create_reply_keyboard(button_labels: list) -> ReplyKeyboardMarkup:
    buttons_per_row = 3
    keyboard = []
    current_row = []

    for label in button_labels:
        current_row.append(KeyboardButton(text=label))
        if len(current_row) == buttons_per_row:
            keyboard.append(current_row)
            current_row = []

    if current_row:
        keyboard.append(current_row)

    keyboard.append([KeyboardButton(text="Назад")])

    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return markup


markup_all_game = create_reply_keyboard(summ_game_list)



but_photo = KeyboardButton(text='Скриншот')
but_accept_game = KeyboardButton(text='Принять игру')
but_pause = KeyboardButton(text='⏸️')
but_escape = KeyboardButton(text='Выключить ПК')

if isTake:
    markup_func = ReplyKeyboardMarkup(keyboard=[[but_photo, but_accept_game],
                                                [but_pause],
                                                [but_escape],
                                                [but_back]],
                                      resize_keyboard=True)
else:
    markup_func = ReplyKeyboardMarkup(keyboard=[[but_photo, but_accept_game],
                                                [but_escape],
                                                [but_back]],
                                      resize_keyboard=True)



but_photo_0 = KeyboardButton(text='Оба')
but_photo_1 = KeyboardButton(text='Основной')
but_photo_2 = KeyboardButton(text='Второй')

if isTake:
    markup_photo = ReplyKeyboardMarkup(keyboard=[[but_photo_2, but_photo_1],
                                                 [but_photo_0],
                                                 [but_back]],
                                       resize_keyboard=True)
else:
    markup_photo = ReplyKeyboardMarkup(keyboard=[[but_photo_1],
                                                 [but_back]],
                                       resize_keyboard=True)


#ESCAPEEEEEEEE
but_tochno = KeyboardButton(text='Точно!')
markup_tochno = ReplyKeyboardMarkup(keyboard=[[but_tochno],
                                              [but_no]],
                                 resize_keyboard=True)

but_tochno_tochno = KeyboardButton(text='Точно точно!')
markup_tochno_tochno = ReplyKeyboardMarkup(keyboard=[[but_tochno_tochno],
                                                     [but_no]],
                                 resize_keyboard=True)

