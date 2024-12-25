from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from config import pupil_data_repo, bot
from phrases import PUPIL_AGE, PUPIL_ERROR_AGE, SCHOOL_TYPE, SCHOOL_REQUEST, ERROR_SCHOOL, GRADE_REQUEST, ERROR_GRADE, \
    EXAM_REQUEST, UNIVERSITY_REQUEST, ERROR_BUTTON, UNIVERSITY_LIST_REQUEST, GUIDE_UNIVERSITY, ERROR_UNIVERSITY, \
    PUPIL_Q1, PUPIL_Q2, PUPIL_Q3, PUPIL_Q4, PUPIL_Q5, PUPIL_Q6, PUPIL_THX
from src.keyboards.pupil_keyboard import pupil_age_keyboard, pupil_school_type_keyboard, school_types_buttons, \
    lyceum_keyboard, gymnasium_keyboard, school_keyboard, school_buttons, gymnasium_buttons, lyceum_buttons, \
    grade_keyboard, request_keyboard, answer_buttons, university_keyboard, university_list, keyboard_q3, keyboard_q5, \
    keyboard_q6, answer_q3, keyboard_q4, answer_q4, answer_q5, answer_q6
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
            exam = "ЕГЭ по информатике?"
        else:
            exam = "ОГЭ по информатике?"
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


@pupil_router.message(StateFilter(Pupil.wait_exam))
async def handle_pupil_exam(message: Message, state: FSMContext):
    """Обрабатывает вопрос о сдаче экзамена пользователя - ученик"""

    chat_id = message.chat.id
    exam = message.text
    if exam in answer_buttons:
        await state.set_state(Pupil.wait_arrival)
        pupil_data_repo.update_field(chat_id, "exam", exam)
        await bot.send_message(
            chat_id=chat_id,
            text=UNIVERSITY_REQUEST,
            reply_markup=request_keyboard()
        )

    else:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_BUTTON
        )


@pupil_router.message(StateFilter(Pupil.wait_arrival))
async def handle_pupil_university(message: Message, state: FSMContext):
    """Обрабатывает вопрос о поступлении в ВУЗ - ученик"""

    chat_id = message.chat.id
    arrival = message.text
    if arrival in answer_buttons:
        pupil_data_repo.update_field(chat_id, "arrival", arrival)
        if arrival == answer_buttons[0]:
            await state.set_state(Pupil.wait_university)
            await state.update_data(check_list=set())
            await bot.send_message(
                chat_id=chat_id,
                text=UNIVERSITY_LIST_REQUEST,
                reply_markup=ReplyKeyboardRemove()
            )
            await bot.send_message(
                chat_id=chat_id,
                text=GUIDE_UNIVERSITY,
                reply_markup=university_keyboard(set())
            )
        else:
            await state.set_state(Pupil.wait_q2)
            await bot.send_message(
                chat_id=chat_id,
                text=PUPIL_Q2,
                reply_markup=request_keyboard()
            )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_BUTTON
        )

@pupil_router.callback_query(StateFilter(Pupil.wait_university), F.data == "next")
async def handle_check_university_next(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    try:
        state_data = await state.get_data()
        check_list = state_data['check_list']
    except:
        check_list = set()
    if len(check_list) == 0:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_UNIVERSITY
        )
    else:
        await state.set_state(Pupil.wait_q1)
        data_base_university = ""
        for i in range(len(university_list)):
            if i in check_list:
                data_base_university += university_list[i]+"; "
        pupil_data_repo.update_field(chat_id, "university", data_base_university)
        await bot.edit_message_text(
            chat_id=chat_id,
            text="Вы выбрали:\n"+data_base_university,
            message_id=callback.message.message_id,
            reply_markup=None
        )
        await bot.send_message(
            chat_id=chat_id,
            text=PUPIL_Q1,
            reply_markup=request_keyboard()
        )


@pupil_router.callback_query(StateFilter(Pupil.wait_university))
async def handle_check_university(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    university = callback.data
    try:
        state_data = await state.get_data()
        check_list = state_data['check_list']
    except:
        check_list = set()
    if int(university) in check_list:
        check_list.remove(int(university))
    else:
        check_list.add(int(university))
    await bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=callback.message.message_id,
        reply_markup=university_keyboard(check_list)
    )


@pupil_router.message(StateFilter(Pupil.wait_q1))
async def handle_pupil_q1(message: Message, state: FSMContext):
    """Планируете поступление на техническую специальность - ученик"""

    chat_id = message.chat.id
    answer = message.text
    if answer in answer_buttons:
        await state.set_state(Pupil.wait_q2)
        pupil_data_repo.update_field(chat_id, "technical_specialty", answer)
        await bot.send_message(
            chat_id=chat_id,
            text=PUPIL_Q2,
            reply_markup=request_keyboard()
        )

    else:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_BUTTON
        )


@pupil_router.message(StateFilter(Pupil.wait_q2))
async def handle_pupil_q2(message: Message, state: FSMContext):
    chat_id = message.chat.id
    answer = message.text
    if answer in answer_buttons:
        await state.set_state(Pupil.wait_q3)
        pupil_data_repo.update_field(chat_id, "IT_live", answer)
        await bot.send_message(
            chat_id=chat_id,
            text=PUPIL_Q3,
            reply_markup=keyboard_q3()
        )

    else:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_BUTTON
        )


@pupil_router.message(StateFilter(Pupil.wait_q3))
async def handle_pupil_q3(message: Message, state: FSMContext):
    chat_id = message.chat.id
    answer = message.text
    if answer in answer_q3:
        await state.set_state(Pupil.wait_q4)
        pupil_data_repo.update_field(chat_id, "interested_IT", answer)
        await bot.send_message(
            chat_id=chat_id,
            text=PUPIL_Q4,
            reply_markup=keyboard_q4()
        )

    else:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_BUTTON
        )


@pupil_router.message(StateFilter(Pupil.wait_q4))
async def handle_pupil_q4(message: Message, state: FSMContext):
    chat_id = message.chat.id
    answer = message.text
    if answer in answer_q4:
        await state.set_state(Pupil.wait_q5)
        pupil_data_repo.update_field(chat_id, "learn_IT", answer)
        await bot.send_message(
            chat_id=chat_id,
            text=PUPIL_Q5,
            reply_markup=keyboard_q5()
        )

    else:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_BUTTON
        )


@pupil_router.message(StateFilter(Pupil.wait_q5))
async def handle_pupil_q5(message: Message, state: FSMContext):
    chat_id = message.chat.id
    answer = message.text
    if answer in answer_q5:
        await state.set_state(Pupil.wait_q6)
        pupil_data_repo.update_field(chat_id, "make_IT", answer)
        await bot.send_message(
            chat_id=chat_id,
            text=PUPIL_Q6,
            reply_markup=keyboard_q6()
        )

    else:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_BUTTON
        )


@pupil_router.message(StateFilter(Pupil.wait_q6))
async def handle_pupil_q5(message: Message, state: FSMContext):
    chat_id = message.chat.id
    answer = message.text
    if answer in answer_q6:
        await state.set_state(Pupil.end)
        pupil_data_repo.update_field(chat_id, "project_IT", answer)
        await bot.send_message(
            chat_id=chat_id,
            text=PUPIL_THX,
            reply_markup=ReplyKeyboardRemove()
        )

    else:
        await bot.send_message(
            chat_id=chat_id,
            text=ERROR_BUTTON
        )
