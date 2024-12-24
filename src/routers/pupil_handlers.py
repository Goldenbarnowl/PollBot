from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import pupil_data_repo, bot
from phrases import PUPIL_AGE, PUPIL_ERROR_AGE, SCHOOL_TYPE
from src.keyboards.pupil_keyboard import pupil_age_keyboard, pupil_school_type_keyboard
from src.keyboards.user_keyboards import role_buttons
from src.states.pupil_states import Pupil
from src.states.user_states import User

pupil_router = Router()


@pupil_router.message(StateFilter(User.wait_role), F.text.in_(role_buttons['pupil']))
async def handle_pupil_role(message: Message, state: FSMContext):
    """Обрабатывает роль пользователя - ученик"""

    await state.set_state(Pupil.wait_age)

    chat_id = message.chat.id

    try:
        response = pupil_data_repo.get_user_by_chat_id(chat_id)
        if not response.data:
            pupil_data_repo.insert_field(chat_id)
    except:
        pass

    await bot.send_message(
        chat_id=chat_id,
        text=PUPIL_AGE,
        reply_markup=pupil_age_keyboard()
    )


@pupil_router.message(StateFilter(Pupil.wait_age))
async def handle_pupil_age(message: Message, state: FSMContext):
    """Обрабатывает возраст пользователя - ученик"""

    chat_id = message.chat.id
    age = message.text

    try:
        age = int(age)
        if (age > 3) and (age < 25):
            pupil_data_repo.update_field(chat_id, "age", age)
        else:
            raise ValueError

        await bot.send_message(
            chat_id=chat_id,
            text=SCHOOL_TYPE,
            reply_markup=pupil_school_type_keyboard()
        )

    except:
        await bot.send_message(
            chat_id=chat_id,
            text=PUPIL_ERROR_AGE
        )
