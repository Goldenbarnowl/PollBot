from aiogram.fsm.state import State, StatesGroup


class Pupil(StatesGroup):
    wait_age = State()
