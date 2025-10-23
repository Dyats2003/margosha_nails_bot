from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я бот записи на маникюр 💅\n\n"
        "Напиши /help, чтобы увидеть команды."
    )


@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start — Начать\n"
        "/help — Помощь\n"
        "/book — Записаться\n"
        "/reschedule — Перенести запись\n"
        "/cancel — Отменить запись"
    )
