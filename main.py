import asyncio
import datetime

from aiogram import executor , types , Dispatcher , Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv
from states import BlankOrder
from aiogram.dispatcher import FSMContext
from models import add_user , get_all_users , add_grade
from services import create_table_link

bot = Bot(token=getenv("TELEGRAM_API_TOKEN"))
dp = Dispatcher(bot , storage=MemoryStorage())

default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

ages = ("до 18" , "18-24" , "24+")

date_format = "%H:%M %d.%m.%Y"

date_string = "09:00 03.12.2022"

next_day_string = "07:00 04.12.2022"

lottery_start_date = datetime.datetime.strptime(date_string , date_format)

next_day = datetime.datetime.strptime(next_day_string , date_format)

phone_numbers = []

telegram_ids = []

admins = [429626527 , 193036673 , 897425801]


async def start(message: types.Message):
    if message.from_user.id in telegram_ids:
        await message.answer("Йоу ты уже зарегался в этой лотерее")
        return

    await message.answer(f"Йоу привет, рады видеть. Скажи, а как тебя зовут? Пожалуйста напиши Имя и Фамилию")
    await BlankOrder.waiting_for_name.set()


async def set_name(message: types.Message , state: FSMContext):
    text = message.text
    await state.update_data(name=text)
    await BlankOrder.waiting_for_age.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for age in ages:
        keyboard.add(age)

    await message.answer("Теперь мне нужно знать твою возрастную группу" , reply_markup=keyboard)


async def set_age(message: types.Message , state: FSMContext):
    text = message.text
    if text not in ages:
        await message.answer("Выбери из представленных возрастных групп")
        return
    await state.update_data(age=text)
    await BlankOrder.waiting_for_phone_number.set()
    await message.answer("Скинь номер бро. В формате 8XXXXXXXXXX" , reply_markup=types.ReplyKeyboardRemove())


async def set_phone_number(message: types.Message , state: FSMContext):
    text = message.text
    if not text.isnumeric():
        await message.answer("Отправь мне только цифры бро")
    elif not text.startswith("8") or len(text) != 11:
        await message.answer("Бро твой номер должен быть в правильном формате 8XXXXXXXXXX")
    elif text in phone_numbers:
        await message.answer("Такой номер у меня есть бро отправь мне другой")
    else:
        phone_numbers.append(text)
        telegram_id = message.from_user.id
        telegram_ids.append(telegram_id)
        data = await state.get_data()
        is_in_lottery = datetime.datetime.now() < lottery_start_date
        is_file_sending = datetime.datetime.now() >= lottery_start_date
        user_id = await add_user({
            "name": data["name"] ,
            "age": data["age"] ,
            "phone_number": text ,
            "telegram_id": telegram_id ,
            "username": message.from_user.username ,
            "is_in_lottery": is_in_lottery ,
            "is_file_sending": is_file_sending
        })
        if is_in_lottery:
            await message.answer(f"Вот вашей лотерейный номер {user_id}")
        else:
            await message.answer("Держи файл")
            await message.answer("https://cloud.mail.ru/public/C8uJ/k7y9bQTFu")
        await state.finish()


async def send_messages(message: types.Message):
    users = await get_all_users()
    for user in users:
        if not user.is_file_sending:
            user.is_file_sending = False
            await bot.send_message(user.telegram_id ,
                                   "Файл для всех участников https://cloud.mail.ru/public/C8uJ/k7y9bQTFu")
    # for t_id in telegram_ids:
    #     await bot.send_message(t_id, "Файл для всех участников https://cloud.mail.ru/public/C8uJ/k7y9bQTFu")


async def send_anket(message: types.Message):
    users = await get_all_users()
    for user in users:
        await bot.send_message(user.telegram_id , "Дайте оценку этому видео от 1 - очень не понравилось до 5 - очень "
                                                  "понравилось")
        await BlankOrder.waiting_for_grade.set(user=user.telegram_id)


async def take_grade(message: types.Message , state: FSMContext):
    try:
        text = int(message.text)
        if text < 1 or text > 5:
            await message.answer("Лучше отправь цифру от 1 одного до 5")
            return
        await add_grade(message.from_user.id , message.text)
        await message.answer("Спасибо за оценку")
        await state.finish()
    except:
        await message.answer("Нам нужна только цифра")


async def get_user_table(message: types.Message):
    await message.answer("Скоро таблица будет готова")
    await message.answer(await create_table_link())


async def send_link_messages():
    while True:
        await asyncio.sleep(10000)
        if datetime.datetime.now() >= lottery_start_date:
            users = await get_all_users()
            for user in users:
                if not user.is_file_sending:
                    await bot.send_message(user.telegram_id ,
                                           "Файл для всех участников https://cloud.mail.ru/public/C8uJ/k7y9bQTFu")
            return


def do_dispatching():
    dp.register_message_handler(start , commands="start")
    dp.register_message_handler(set_name , state=BlankOrder.waiting_for_name)
    dp.register_message_handler(set_age , state=BlankOrder.waiting_for_age)
    dp.register_message_handler(set_phone_number , state=BlankOrder.waiting_for_phone_number)
    dp.register_message_handler(send_messages , commands="send_messages" , user_id=admins)
    dp.register_message_handler(get_user_table , commands="table" , user_id=admins)
    dp.register_message_handler(send_anket, commands="anket", user_id=admins)
    dp.register_message_handler(take_grade, state=BlankOrder.waiting_for_grade)


if __name__ == "__main__":
    # Запуск бота
    do_dispatching()
    executor.start_polling(dp , skip_updates=True)
