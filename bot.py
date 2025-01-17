# bot.py
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from config import BOT_TOKEN
from database import init_db
from handlers import start, handle_message, add_qa_pair_handler, help_command
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Инициализация базы данных
    conn, cursor = init_db()

    # Регистрация обработчиков
    dp.message.register(start, Command("start"))
    dp.message.register(help_command, Command("help"))
    dp.message.register(add_qa_pair_handler, Command("add"))
    dp.message.register(handle_message, F.text & ~F.text.startswith('/'))

    # Запуск бота
    logging.info("Бот запущен и ожидает сообщений...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())