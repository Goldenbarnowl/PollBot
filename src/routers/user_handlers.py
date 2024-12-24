from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import bot, users_data_repo
from phrases import PERS_DATA_REQUEST, YOU_ROLE, NAME_REQUEST, ERROR_NAME
from src.keyboards.user_keyboards import give_phone_keyboard, role_keyboard
from src.states.user_states import User

user_router = Router()


def remove_leading_plus(s):
    """
    Удаляет первый символ '+' из строки
    Приводит номера телефонов к единому стандарту
    """
    # Проверяем, начинается ли строка с символа '+'
    if s.startswith('+'):
        # Убираем первый символ
        return s[1:]
    return s  # Возвращаем строку без изменений, если первого символа нет


@user_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await state.set_state(User.wait_phone_number)
    chat_id = message.from_user.id
    try:
        response = users_data_repo.get_user_by_chat_id(chat_id)
        if not response.data:
            users_data_repo.insert_field(chat_id, 'reg_date', str(message.date))
    except:
        pass
    await bot.send_message(
        chat_id=chat_id,
        text=PERS_DATA_REQUEST,
        reply_markup=give_phone_keyboard()
    )


@user_router.message(StateFilter(User.wait_phone_number), F.content_type == "contact")
async def handle_contact(message: Message, state: FSMContext):
    """Обрабатывает контакт пользователя"""

    await state.set_state(User.wait_name)

    contact = message.contact
    chat_id = message.chat.id

    # Проверка, что tg_phone принадлежит пользователю
    if contact.user_id != message.from_user.id:
        await bot.send_message(
            chat_id=chat_id,
            text="Нажмите на кнопку «Поделиться номером телефона»",
        )
        return

    users_data_repo.update_field(chat_id, "tg_phone", remove_leading_plus(contact.phone_number))

    await bot.send_message(
        chat_id=chat_id,
        text=NAME_REQUEST,
        reply_markup=ReplyKeyboardRemove()
    )


@user_router.message(StateFilter(User.wait_name))
async def handle_name(message: Message, state: FSMContext):
    """Обрабатывает имя пользователя"""

    await state.set_state(User.wait_role)

    chat_id = message.chat.id
    name = message.text

    if name:
        users_data_repo.update_field(chat_id, "name", name)
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_NAME
        )
    await bot.send_message(
        chat_id=chat_id,
        text=YOU_ROLE,
        reply_markup=role_keyboard()
    )
