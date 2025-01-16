from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.utils.db import is_user_registered


class RegistrationCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        # Если это команда /start, пропускаем дальнейшую проверку
        if event.text and event.text.startswith("/start"):
            return await handler(event, data)
        # Получаем контекст FSM, если он существует
        fsm_context: FSMContext = data.get('state')
        # Если контекст FSM существует, проверяем текущее состояние
        if fsm_context:
            state = await fsm_context.get_state()
            # Если пользователь в процессе регистрации (есть состояние), пропускаем проверку
            if state is not None:
                return await handler(event, data)
        # Проверка регистрации пользователя, если FSM контекст не используется или нет состояния
        user_id = event.from_user.id
        if not is_user_registered(user_id):
            await event.answer(
                "Вы не зарегистрированы! Используйте команду /start для регистрации.")
            return
        # Если пользователь зарегистрирован, продолжаем выполнение хендлера
        return await handler(event, data)
