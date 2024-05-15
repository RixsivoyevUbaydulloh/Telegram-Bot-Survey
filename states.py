from aiogram.dispatcher.filters.state import State, StatesGroup


class Register(StatesGroup):
    name = State()
    number = State()
    age = State()
    profession = State()
    gender = State()
