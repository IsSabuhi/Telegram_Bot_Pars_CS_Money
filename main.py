import json
import time
from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink, hbold

import config
from parsing import collect_data


bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Ножи', 'Снайперские винтовки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Выберите категорию", reply_markup=keyboard)


@dp.message_handler(Text(equals='Ножи'))
async def get_discount_knives(message: types.Message):
    await message.answer('Пожалуйста подождите ...')

    collect_data(cat_type=2)

    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
                f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
                f'{hbold("Цена: ")}{item.get("item_price")}'

            if index%20 == 0:
                time.sleep(3)

            await message.answer(card)


@dp.message_handler(Text(equals='Снайперские винтовки'))
async def get_discount_gloves(message: types.Message):
    await message.answer('Пожалуйста подождите ...')

    collect_data(cat_type=4)

    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
                   f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
                   f'{hbold("Цена: ")}{item.get("item_price")}'

            if index % 20 == 0:
                time.sleep(3)

            await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()