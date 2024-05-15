from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, ReplyKeyboardRemove
from database import DataBase
from keyboards import generate_start_button, generate_gender_buttons
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from states import Register

bot = Bot(token='7049607831:AAH9_rudg6Edv6LfTAnVrha7Kb2bEGXQfQQ')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DataBase()


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    chat_id = message.chat.id
    db.create_users_table()
    user = db.get_user_by_chat_id(chat_id)
    if user:
        if user[2] is None or user[3] is None or user[4] is None or user[5] is None:
            await bot.send_message(chat_id, 'You have not finished the survey. You can try again!',
                                   reply_markup=generate_start_button())
        else:
            await bot.send_message(chat_id, 'You have already completed the survey. All information has been saved!')
    else:
        db.first_register_user(chat_id)
        await bot.send_message(chat_id, 'Complete survey. With using buttoon below.',
                               reply_markup=generate_start_button())


@dp.message_handler(regexp='Start Registration')
async def start_register(message: Message):
    chat_id = message.chat.id
    await Register.name.set()
    await bot.send_message(chat_id, 'Enter your name:')


@dp.message_handler(state=Register.name)
async def get_name_ask_number(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(name=message.text)
    await Register.gender.set()
    await bot.send_message(chat_id, 'Enter the phone number:')


@dp.message_handler(regexp=r'^\+998[0-9]{9}$', state=Register.gender)
async def get_number_ask_gender(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(number=message.text)
    await Register.age.set()
    await bot.send_message(chat_id, 'Enter your gender:', reply_markup=generate_gender_buttons())


@dp.message_handler(regexp='(Male|Female)', state=Register.gender)
async def get_gender_ask_age(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(gender=message.text)
    await Register.age.set()
    await bot.send_message(chat_id, 'Enter your age:', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(regexp='\d\d', state=Register.age)
async def get_age_ask_profession(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(age=message.text)
    await Register.profession.set()
    await bot.send_message(chat_id, 'Enter your occupation: ')


@dp.message_handler(state=Register.profession)
async def get_profession_save_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    profession = message.text
    data = await state.get_data()
    db.save_data(chat_id, data['name'], data['number'], data['gender'], data['age'], profession)
    await state.finish()
    await bot.send_message(chat_id, 'You have finished the registration fully!')
    await command_start(message)


@dp.message_handler(commands=['export'])
async def export_data(message: Message):
    chat_id = message.chat.id
    db.get_data_for_excel()
    with open('result.xlsx', mode='rb') as file:
        await bot.send_document(chat_id, file)


executor.start_polling(dp)
