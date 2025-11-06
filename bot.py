import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import settings
from handlers.start_help import router as start_router
from handlers.services_menu import router as services_router


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(services_router)
    print("Bot is running (polling).")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
