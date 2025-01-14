from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_gigachat import GigaChat
from bot.utils.config import GigaChatKey
from bot.utils.db import get_user_profile

# Настройка API ключа для GigaChat
GigaChatKey = GigaChatKey
llm_adv = GigaChat(credentials=GigaChatKey,
                   model='GigaChat:latest',
                   verify_ssl_certs=False)

# Промпты для генерации сообщений
motivation_prompt_template = """
Ты — вдохновляющий тренер, который помогает людям оставаться мотивированными.
Пользователь имеет уровень подготовки: {level} и стремится достичь следующей цели: {goal}. 
Создай мотивационное сообщение, которое поднимет настроение пользователю и поможет ему продолжать двигаться к своей цели.
 Убедись, что сообщение соответствует его уровню подготовки и цели.
"""

advice_prompt_template = """
Ты — профессиональный тренер, который даёт ценные советы.
 Пользователь имеет уровень подготовки: {level} и стремится достичь следующей цели: {goal}. 
Дай практический совет, который поможет пользователю продвинуться на пути к своей цели.
Убедись, что совет соответствует его текущему уровню подготовки и конкретной цели.
"""


# Создаём цепочки
motivation_prompt = PromptTemplate.from_template(motivation_prompt_template)
advice_prompt = PromptTemplate.from_template(advice_prompt_template)

motivation_chain = LLMChain(llm=llm_adv, prompt=motivation_prompt)
advice_chain = LLMChain(llm=llm_adv, prompt=advice_prompt)

router = Router()


@router.message(Command("motivation"))
async def send_motivation(message: Message):
    user_id = message.from_user.id

    # Получаем данные пользователя через вашу функцию
    user_profile = get_user_profile(user_id)

    if not user_profile:
        await message.answer("Ваш профиль не найден. Пожалуйста, заполните данные в настройках.")
        return

    try:
        # Генерация мотивационного сообщения
        motivation_message = motivation_chain.invoke(
            {"level": user_profile["level"], "goal": user_profile["goal"]})
        await message.answer(f"Ваше мотивационное сообщение:\n\n{motivation_message['text']}", parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка генерации мотивационного сообщения: {e}")
        await message.answer("Не удалось создать мотивационное сообщение. Попробуйте позже.")


@router.message(Command("advice"))
async def send_advice(message: Message):
    user_id = message.from_user.id

    # Получаем данные пользователя через вашу функцию
    user_profile = get_user_profile(user_id)

    if not user_profile:
        await message.answer("Ваш профиль не найден. Пожалуйста, заполните данные в настройках.")
        return

    try:
        # Генерация совета
        advice_message = advice_chain.invoke(
            {"level": user_profile["level"], "goal": user_profile["goal"]})
        await message.answer(f"Ваш совет:\n\n{advice_message['text']}", parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка генерации совета: {e}")
        await message.answer("Не удалось создать совет. Попробуйте позже.")
