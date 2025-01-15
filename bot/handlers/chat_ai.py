import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_gigachat import GigaChat
from bot.utils.config import GigaChatKey
# Словарь для хранения памяти пользователей
user_histories = {}


logger = logging.getLogger(__name__)

# Настройка API ключа для GigaChat
GigaChatKey = GigaChatKey
llm = GigaChat(credentials=GigaChatKey, model='GigaChat:latest', verify_ssl_certs=False)

# Промпт для общения
base_prompt_template = """
Ты опытный тренер по бегу! Ниже представлена история вашего разговора с пользователем:
{chat_history}
User: {input}
Assistant:
"""
prompt = PromptTemplate.from_template(base_prompt_template)

router = Router()

@router.message(Command("ask_ai"))
async def ai_assistant(message: Message):
    user_input = message.text[len("/ask_ai "):].strip()

    if not user_input:
        await message.answer("Пожалуйста, напишите ваш вопрос или запрос.")
        return

    # Получаем историю пользователя
    user_id = message.from_user.id
    chat_history = get_user_history(user_id)

    # Формируем цепочку
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Добавляем текущий запрос в историю
    chat_history.append(f"User: {user_input}")

    # Подготовка контекста для запроса
    chat_context = "\n".join(chat_history)
    try:
        response = llm_chain.run(chat_history=chat_context, input=user_input)
        # Добавляем ответ ассистента в историю
        chat_history.append(f"Assistant: {response}")
        await message.answer(f"Ответ от ассистента: {response}", parse_mode="Markdown")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        logger.error(f"Ошибка генерации ответа {user_id}: {e}")
        await message.answer("Произошла ошибка при обработке вашего запроса.")

# Функция для получения или создания истории пользователя
def get_user_history(user_id):
    """Получение истории пользователя. Если её нет, создаётся новая."""
    if user_id not in user_histories:
        user_histories[user_id] = []
    return user_histories[user_id]