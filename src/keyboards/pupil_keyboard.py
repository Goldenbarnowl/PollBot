from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

school_types_buttons = {"school": "🏫 Школа", "lyceum": "🏫 Лицей", "gymnasium": "🏫 Гимназия"}


def pupil_age_keyboard():
    pupil_age_keyboard_builder = ReplyKeyboardBuilder()
    for age in range(7, 20):
        button = KeyboardButton(text=str(age))
        if age in [11, 16]:
            pupil_age_keyboard_builder.row(button)
        else:
            pupil_age_keyboard_builder.add(button)
    return pupil_age_keyboard_builder.as_markup(resize_keyboard=True, is_persistent=True)


def pupil_school_type_keyboard():
    pupil_school_type_keyboard_builder = ReplyKeyboardBuilder()
    for school_type in school_types_buttons:
        button = KeyboardButton(text=school_types_buttons[school_type])
        pupil_school_type_keyboard_builder.row(button)
    return pupil_school_type_keyboard_builder.as_markup(resize_keyboard=True, is_persistent=True)