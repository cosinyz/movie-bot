import asyncio
import os
import random

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎬 Случайный фильм")],
        [KeyboardButton(text="⭐ Топ фильмов")],
        [KeyboardButton(text="ℹ️ Помощь")]
    ],
    resize_keyboard=True
)

MOVIES = [
    "Интерстеллар (2014) — научная фантастика о времени, любви и космосе.",
    "1+1 (2011) — трогательная история дружбы и неожиданных перемен.",
    "Начало (2010) — команда специалистов проникает в чужие сны.",
    "Зеленая миля (1999) — сильная драма о сострадании и человечности.",
    "Паразиты (2019) — сатирический триллер о двух семьях и социальном неравенстве.",
]

TOP_MOVIES = (
    "⭐ Популярные фильмы:\n"
    "1. Побег из Шоушенка (1994)\n"
    "2. Крестный отец (1972)\n"
    "3. Темный рыцарь (2008)\n"
    "4. Интерстеллар (2014)\n"
    "5. Паразиты (2019)"
)


@router.message(Command(commands=["start"]))
async def start_command(message: Message):
    await message.answer(
        f"Здравствуй, {message.from_user.first_name}!\n"
        "Я кино-бот: подберу случайный фильм и покажу популярную подборку.",
        reply_markup=main_keyboard,
    )

@router.message(Command(commands=["help"]))
async def help_command(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start — начать работу с ботом\n"
        "/help — показать эту справку\n"
        "/random — получить случайный фильм\n"
        "/top — показать подборку популярных фильмов",
        reply_markup=main_keyboard,
    )

@router.message(Command(commands=["random"]))
async def random_command(message: Message):
    await message.answer(
        f"🎬 Совет дня:\n{random.choice(MOVIES)}",
        reply_markup=main_keyboard,
    )


@router.message(Command(commands=["top"]))
async def top_command(message: Message):
    await message.answer(TOP_MOVIES, reply_markup=main_keyboard)


@router.message(F.text == "🎬 Случайный фильм")
async def random_button(message: Message):
    await random_command(message)


@router.message(F.text == "⭐ Топ фильмов")
async def top_button(message: Message):
    await top_command(message)


@router.message(F.text == "ℹ️ Помощь")
async def help_button(message: Message):
    await help_command(message)


@router.message(F.text.casefold() == "привет")
async def greeting_message(message: Message):
    await message.answer("Привет! Рад тебя видеть в кино-клубе 🎬", reply_markup=main_keyboard)


@router.message(F.text.casefold() == "спасибо")
async def thanks_message(message: Message):
    await message.answer("Пожалуйста! Хорошего просмотра 🍿", reply_markup=main_keyboard)


@router.message()
async def unknown_message(message: Message):
    await message.answer(
        "Кажется, этот сценарий еще не попал в прокат. Воспользуйся /help или кнопками ниже.",
        reply_markup=main_keyboard,
    )


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())