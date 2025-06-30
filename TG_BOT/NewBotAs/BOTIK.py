import asyncio
import webbrowser
import pyautogui
import psutil
import os

from time import sleep
from subprocess import run, Popen
from datetime import datetime
from win32gui import IsWindowVisible, FindWindow, PostMessage
from win32con import WM_CLOSE
from json import loads
from uuid import getnode
from dotenv import load_dotenv
from mss import mss
from mss.tools import to_png
from screeninfo import get_monitors

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message, FSInputFile

from NewBotAs.FOR_BOT.Button.automac import go_auto_mac
from FOR_BOT.Button.button import *



load_dotenv('FOR_BOT/.env')
bot = Bot(os.getenv('BOT_API')) #TOKEN
dp = Dispatcher()


MY = os.path.join(os.path.dirname(__file__), 'FOR_BOT/Screenshots/MY')
TV = os.path.join(os.path.dirname(__file__), 'FOR_BOT/Screenshots/TV')
ALL = os.path.join(os.path.dirname(__file__), 'FOR_BOT/Screenshots/ALL')
KEY_CODE = os.path.join(os.path.dirname(__file__), 'KEY_CODE.txt')



async def isChageMac():
    if os.path.isfile('FOR_BOT/Button/automac.py'):
        go_auto_mac()
        sleep(2)
        os.remove('FOR_BOT/Button/automac.py')
    else: pass


def other_game_func():
    other = []
    game = loads(os.getenv('GAME_OTHER'))
    for i in game:
        other.append(i)
    return other

def steam_game_func():
    steam = []
    for i in loads(os.getenv('GAME_STEAM')):
        steam.append(i)
    return steam

return_other_game = other_game_func()
return_steam_game = steam_game_func()
summ_game_list = return_steam_game + return_other_game


async def isGame(message: Message):
    if message.text in summ_game_list:
        await open_game(message, return_steam_game, return_other_game)


async def isClickSecond(message: Message):
    if message.text == "⏸️" and os.getenv('MONITOR_SECOND') == '1':
        await pause(message)


def MAC(my_mac, env_mac):
    last_line = ''
    with open('FOR_BOT/requirements.txt', "r") as file:
        last_line = file.readlines()[-1]
    ll = str(last_line.split('==')[-1]).strip()
    return ll == my_mac == env_mac


async def isStop():
    my_mac = str(getnode())
    env_mac = str(int(os.getenv('MAC'), 16))
    txt_mac = MAC(my_mac, env_mac)
    if not txt_mac:
        await dp.stop_polling()
    else:
        await bot.send_message(int(os.getenv('YOUR_TG_ID')), text=f'Твой пк запущен({os.getenv('NAME_BOT')})')


#START
@dp.message(Command("start"))
async def start(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        msg = f'Привет, я {os.getenv('NAME_BOT')}! Чем могу быть полезен?'

        await message.answer(msg, reply_markup=markup_app, parse_mode='HTML')

    else:
        await message.answer('Пока!)')


@dp.message(F.text == 'Игры')
async def change_game(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        await message.answer('Выбери игру', reply_markup=markup_all_game)
    else:
        await message.answer('Пока!)')


@dp.message(F.text == 'Функции')
async def change_func(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        await message.answer('Выбери функцию', reply_markup=markup_func)
    else:
        await message.answer('Пока!)')


@dp.message(F.text == 'Скриншот')
async def take_photo(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        await message.answer('Выбери экран', reply_markup=markup_photo, parse_mode='HTML')
    else:
        await message.answer('Пока!)')


@dp.message(F.text == 'Основной')
async def take_photo_1(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        os.makedirs(name=MY, exist_ok=True)

        with mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            t = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = os.path.join(MY, f'screenshot_{t}.png')

            to_png(sct_img.rgb, sct_img.size, output=filename)
            await bot.send_photo(message.chat.id, FSInputFile(filename))
    else:
        await message.answer('Пока!)')


@dp.message(F.text == 'Второй')
async def take_photo_2(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        try:
            os.makedirs(name=TV, exist_ok=True)

            with mss() as sct:
                monitor = sct.monitors[2]
                sct_img = sct.grab(monitor)
                t = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = os.path.join(TV, f'screenshot_{t}.png')

                to_png(sct_img.rgb, sct_img.size, output=filename)
                await bot.send_photo(message.chat.id, FSInputFile(filename))

        except:
            await message.answer('У вас один монитор')
    else:
        await message.answer('Пока!)')


@dp.message(F.text == 'Оба')
async def take_photo_0(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        try:
            os.makedirs(name=ALL, exist_ok=True)

            with mss() as sct:
                monitor = sct.monitors[0]
                sct_img = sct.grab(monitor)
                t = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = os.path.join(ALL, f'screenshot_{t}.png')

                to_png(sct_img.rgb, sct_img.size, output=filename)
                await bot.send_photo(message.chat.id, FSInputFile(filename))

        except:
            await message.answer('У вас один монитор, используйте функцию ОСНОВНОЙ')
    else:
        await message.answer('Пока!)')


@dp.message(F.text == 'Принять игру')
async def accept_game(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        width, height = pyautogui.size()

        center_x = width // 2
        center_y = height // 2

        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()

        await message.answer('Игра принята', reply_markup=markup_func, parse_mode='HTML')
    else:
        await message.answer('Пока!)')


@dp.message(isClickSecond)
async def pause(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        second_monitor = get_monitors()[1]
        width, height = second_monitor.width, second_monitor.height

        pyautogui.moveTo((width // 2) + second_monitor.x, (height // 2) + second_monitor.y)
        pyautogui.click()
        await message.answer('ПАУЗА', reply_markup=markup_func, parse_mode='HTML')
    else:
        await message.answer('Пока!)')


@dp.message(F.text == 'Выключить ПК')
async def esc_func(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        await message.answer('Вы точно хотите этого?', reply_markup=markup_tochno)
    else:
        await message.answer('Пока!)')


@dp.message(F.text == 'Точно!')
async def tochno_func(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        await message.answer('Точно точно?', reply_markup=markup_tochno_tochno)
    else:
        await message.answer('Пока!)')


@dp.message(F.text == 'Точно точно!')
async def tochno_tochno_func(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        await message.answer('До уничтожения:', reply_markup=markup_app)
        await asyncio.sleep(0.5)
        await message.answer('3', reply_markup=markup_app)
        await asyncio.sleep(0.3)
        await message.answer('2', reply_markup=markup_app)
        await asyncio.sleep(0.3)
        await message.answer('1', reply_markup=markup_app)
        run(['shutdown', '/s', '/t', '1'], check=True)
    else:
        await message.answer('Пока!)')


@dp.message(F.text.startswith(('Открой', 'Найди', 'Найти', 'Поиск', 'Открыть')))
async def open_yandex(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
    
        m = ' '.join(message.text.split(' ')[1::])
        webbrowser.open(f"https://yandex.ru/search/?text={m.replace(' ', '+')}")
        await message.answer('Ответ найден!', parse_mode='HTML')
    else:
        await message.answer('Пока!)')


@dp.message(F.text.startswith(f"http"))
async def open_link(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        webbrowser.open(message.text)
        await message.answer('Ссылка открыта!', parse_mode='HTML')
    else:
        await message.answer('Пока!)')


@dp.message(isGame)
async def open_game(message: Message, steam_game: return_steam_game, other_game: return_other_game):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        text = message.text

        if text in steam_game:

            for i in steam_game:
                if text == i:
                    key = loads(os.getenv('GAME_STEAM'))[i]
                    haunt = IsWindowVisible(FindWindow(None, i))

                    if haunt:
                        PostMessage(FindWindow(None, i), WM_CLOSE, 0, 0)
                        await message.answer(f'{i} закрыта')

                    else:
                        try:
                            Popen([os.getenv('STEAM'), "-applaunch", key])
                            await message.answer(f"{i} открыта")
                        except:
                            await message.answer('Не верный ID игры или название')

        else:

            for i in other_game:
                if text == i:
                    key = loads(os.getenv('GAME_OTHER'))[i].replace('---', '//')
                    haunt = IsWindowVisible(FindWindow(None, i))

                    if haunt:
                        for proc in psutil.process_iter(['pid', 'name']):
                            if proc.info['name'] == key.split('//')[-1]:
                                proc.kill()
                        await message.answer(f'{i} закрыт')

                    else:
                        try:
                            Popen([key], shell=True)
                            await message.answer(f'{i} открыт')
                        except:
                            await message.answer('Не верный путь')
    else:
        await message.answer('Пока!)')



# BACK OR NONE
@dp.message(F.text == 'Назад')
async def back_menu(message: Message):
    if message.from_user.id == int(os.getenv('YOUR_TG_ID')):
        await start(message)
    else:
        await message.answer('Пока!)')



async def main():
    #await isChageMac()
    #await isStop()
    await bot.delete_webhook(drop_pending_updates=True) #Пропуск Сообщений до включение кода
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
