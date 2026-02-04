# handlers/commands.py

import logging
from state_helpers import clear_history, show_screen, clear_user_date
from util.util import load_message, send_photo, send_text, show_main_menu, send_text_buttons, Dialog
from dialog_state import KEY_MODE, MODE_MAIN, MODE_GPT, MODE_DATE, MODE_MESSAGE, MODE_PROFILE, FORM_QUESTIONS, \
    MODE_OPENER, FORM_QUESTIONS_OPENER

log = logging.getLogger(__name__)

async def start(update, context):
    context.chat_data[KEY_MODE] = MODE_MAIN
    await show_screen(update, context, MODE_MAIN)

    await show_main_menu(update, context, {
        "start": "Главное меню бота",
        "profile": "генерация Tinder-профля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос чату GPT 🧠"
    })

async def gpt(update, context):
    context.chat_data[KEY_MODE] = MODE_GPT
    await show_screen(update, context, MODE_GPT)

async def date(update, context):
    context.chat_data[KEY_MODE] = MODE_DATE

    text = load_message(MODE_DATE)
    await send_photo(update, context, MODE_DATE)
    await send_text_buttons (update, context, text, {
        "date_grande":"Ариана Гранде",
        "date_robbie":"Марго Робби",
        "date_zendaya":"Зендея",
        "date_gosling":"Райан Гослинг",
        "date_hardy":"Том Харди",
        "date_make_profile": "Сформировать мой профиль 🧾"
    })

async def message(update, context):
    context.chat_data[KEY_MODE] = MODE_MESSAGE

    text = load_message(MODE_MESSAGE)
    await send_photo(update, context, MODE_MESSAGE)
    await send_text_buttons (update, context, text, {
        "message_next":"Следующее сообщение",
        "message_date":"Пригласить на свидание"
    })
    clear_history(context)

async def profile(update, context):
    context.chat_data[KEY_MODE] = MODE_PROFILE
    await show_screen(update, context, MODE_PROFILE)
    clear_user_date(context)
    first_question = FORM_QUESTIONS["age"]
    await send_text(update, context, first_question)

async def opener(update, context):
    context.chat_data[KEY_MODE] = MODE_OPENER
    await show_screen(update, context, MODE_OPENER)
    clear_user_date(context)
    first_question = FORM_QUESTIONS_OPENER["name"]
    await send_text(update, context, first_question)


