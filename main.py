import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from translate import Translator

API_TOKEN = '7769073713:AAENJcwZxz37i0z2Vrx9RngrnUQbb1-loNg'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Global variable to store the current translation mode
current_mode = 'en_to_ru'  # Default mode: English to Russian

# Inline keyboard buttons
button_1 = InlineKeyboardButton('Англ🇺🇸-Русс🇷🇺', callback_data='en_to_ru')
button_2 = InlineKeyboardButton('Русс🇷🇺-Англ🇺🇸', callback_data='ru_to_en')
keyboard = InlineKeyboardMarkup().add(button_1, button_2)


def is_russian(text):
    return any(char in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" for char in text.lower())


def is_english(text):
    return any(char in "abcdefghijklmnopqrstuvwxyz" for char in text.lower())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Send a welcome message with inline buttons."""
    await message.reply("Привет! Я переводчик бот. Выберите режим перевода:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data in ['en_to_ru', 'ru_to_en'])
async def set_translation_mode(callback_query: types.CallbackQuery):
    """Set the translation mode based on the button clicked."""
    global current_mode
    current_mode = callback_query.data

    if current_mode == 'en_to_ru':
        await callback_query.message.answer("Режим перевода: Английский🇺🇸 -> Русский🇷🇺")
    elif current_mode == 'ru_to_en':
        await callback_query.message.answer("Режим перевода: Русский🇷🇺 -> Английский🇺🇸")

    await callback_query.answer()  # Confirm button click


@dp.message_handler()
async def translate_message(message: types.Message):
    """Translate the message text based on the current translation mode."""
    global current_mode

    if current_mode == 'en_to_ru':
        if is_russian(message.text):
            await message.answer("Вы выбрали режим Английский🇺🇸 -> Русский🇷🇺, но отправили русское слово. Хотите изменить язык?", reply_markup=keyboard)
            return
        translator = Translator(from_lang="english", to_lang="russian")
    elif current_mode == 'ru_to_en':
        if is_english(message.text):
            await message.answer("Вы выбрали режим Русский🇷🇺 -> Английский🇺🇸, но отправили английское слово. Хотите изменить язык?", reply_markup=keyboard)
            return
        translator = Translator(from_lang="russian", to_lang="english")

    try:
        translation = translator.translate(message.text)
        await message.answer(translation)
    except Exception as e:
        logging.error(f"Translation error: {e}")
        await message.answer("Произошла ошибка при переводе. Пожалуйста, попробуйте снова.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
