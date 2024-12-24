from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import pupil_data_repo, bot
from phrases import PUPIL_AGE, PUPIL_ERROR_AGE, SCHOOL_TYPE, SCHOOL_REQUEST, ERROR_SCHOOL, GRADE_REQUEST, ERROR_GRADE, \
    EXAM_REQUEST
from src.keyboards.pupil_keyboard import pupil_age_keyboard, pupil_school_type_keyboard, school_types_buttons, \
    lyceum_keyboard, gymnasium_keyboard, school_keyboard, school_buttons, gymnasium_buttons, lyceum_buttons, \
    grade_keyboard, request_keyboard
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

        await state.set_state(Pupil.wait_school_type)
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


@pupil_router.message(StateFilter(Pupil.wait_school_type), F.text.in_([school_types_buttons['school'], school_types_buttons['lyceum'], school_types_buttons['gymnasium']]))
async def handle_pupil_school_type(message: Message, state: FSMContext):
    """Обрабатывает тип школы пользователя - ученик"""

    await state.set_state(Pupil.wait_school)

    chat_id = message.chat.id
    school_type = message.text

    if school_type == school_types_buttons['school']:
        await bot.send_message(
            chat_id=chat_id,
            text=SCHOOL_REQUEST,
            reply_markup=school_keyboard()
        )

    elif school_type == school_types_buttons['lyceum']:
        await bot.send_message(
            chat_id=chat_id,
            text=SCHOOL_REQUEST,
            reply_markup=lyceum_keyboard()
        )

    elif school_type == school_types_buttons['gymnasium']:
        await bot.send_message(
            chat_id=chat_id,
            text=SCHOOL_REQUEST,
            reply_markup=gymnasium_keyboard()
        )


@pupil_router.message(StateFilter(Pupil.wait_school))
async def handle_pupil_school(message: Message, state: FSMContext):
    """Обрабатывает учебное заведение пользователя - ученик"""

    chat_id = message.chat.id
    school = message.text

    if (school in school_buttons) or (school in gymnasium_buttons) or (school in lyceum_buttons):

        await state.set_state(Pupil.wait_grade)
        pupil_data_repo.update_field(chat_id, "school", school)

        await bot.send_message(
            chat_id=chat_id,
            text=GRADE_REQUEST,
            reply_markup=grade_keyboard()
        )

    else:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_SCHOOL
        )


@pupil_router.message(StateFilter(Pupil.wait_grade))
async def handle_pupil_grade(message: Message, state: FSMContext):
    """Обрабатывает класс в школе пользователя - ученик"""

    chat_id = message.chat.id
    grade = message.text

    try:
        grade = int(grade)
        if (grade > 0) and (grade < 12):
            pupil_data_repo.update_field(chat_id, "grade", grade)
        else:
            raise ValueError
        await state.set_state(Pupil.wait_exam)
        if grade > 9:
            exam = "ЕГЭ"
        else:
            exam = "ОГЭ"
        await bot.send_message(
            chat_id=chat_id,
            text=EXAM_REQUEST+exam,
            reply_markup=request_keyboard()
        )
    except:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_GRADE
        )

