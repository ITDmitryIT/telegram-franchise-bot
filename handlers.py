# handlers.py
from aiogram import types, F
from aiogram.filters import Command
import logging
import traceback
import random
from database import add_qa_pair, get_all_qa_pairs, get_answers_for_question
from model import train_model, predict_answer
from utils import preprocess_text
from config import ADMIN_ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(message: types.Message):
    await message.reply('Привет! Я бот-помощник по вопросам франшизы. Задайте мне вопрос.')


async def handle_message(message: types.Message, conn, cursor, tfidf_vectorizer, model):
    try:
        user_message = message.text
        logging.info(f"Получено сообщение: {user_message}")

        # Проверяем базу данных на точное совпадение
        answers = get_answers_for_question(cursor, user_message)
        if answers:
            response = random.choice(answers)[0]
        else:
            # Используем модель, если точного совпадения нет
            processed_question = preprocess_text(user_message)
            response = predict_answer(tfidf_vectorizer, model, processed_question)

        await message.reply(response)
    except Exception as e:
        logging.error(f"Ошибка: {e}\n{traceback.format_exc()}")
        await message.reply("Произошла ошибка. Попробуйте позже.")


async def add_qa_pair_handler(message: types.Message, conn, cursor):
    if message.from_user.id == ADMIN_ID:
        try:
            text = message.text.replace('/add', '').strip()
            if '|' not in text:
                await message.reply("Неправильный формат. Используйте: /add вопрос | ответ")
                return

            question, answer = text.split('|', maxsplit=1)
            question = question.strip()
            answer = answer.strip()

            if not question or not answer:
                await message.reply("Вопрос и ответ не могут быть пустыми.")
                return

            add_qa_pair(conn, cursor, question, answer)

            df = get_all_qa_pairs(conn)
            if df['answer'].nunique() >= 2:
                df['processed_question'] = df['question'].apply(preprocess_text)
                tfidf_vectorizer, model = train_model(df)
                await message.reply("Пара вопрос-ответ добавлена и модель переобучена.")
            else:
                await message.reply(
                    "Пара вопрос-ответ добавлена. Модель не переобучена, так как требуется как минимум два разных ответа.")
        except Exception as e:
            await message.reply(f"Ошибка: {e}")
    else:
        await message.reply("У вас нет прав для выполнения этой команды.")


async def help_command(message: types.Message):
    help_text = """
Доступные команды:
/start - начать диалог
/help - помощь
/add - добавить вопрос и ответ (только для администратора)
    """
    await message.reply(help_text)