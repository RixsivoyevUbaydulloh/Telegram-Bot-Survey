from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def generate_start_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='Start Registration')
    markup.add(btn)
    return markup


def generate_gender_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    male = KeyboardButton(text='Male')
    female = KeyboardButton(text='Female')
    markup.row(male, female)
    return markup