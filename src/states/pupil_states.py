from aiogram.fsm.state import State, StatesGroup


class Pupil(StatesGroup):
    wait_age = State()
    wait_school_type = State()
    wait_school = State()
    wait_grade = State()
    wait_exam = State()
