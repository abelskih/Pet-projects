# handlers/callbacks.py

from dialog_state import KEY_DIALOG_LIST, FORM_STEPS, FORM_QUESTIONS, KEY_DATE_PROFILE, FORM_QUESTIONS_OPENER
from state_helpers import answer_with_loading, get_user_date, run_form_step, clear_user_date
from util.util import send_text, send_text_buttons, send_photo, send_html, load_prompt

async def hello_button(update, context):
    cq = update.callback_query
    await cq.answer()
    query = cq.data

    if query == "start":
        await cq.edit_message_reply_markup(reply_markup=None)
        await send_text(update, context, "Процесс запущен")
        await send_text_buttons(update, context, "Выбери картинку:", {
            "photo:gpt": "gpt",
            "photo:date": "date",
            "photo:error": "error",
        })
        return

    if query == "stop":
        await cq.edit_message_reply_markup(reply_markup=None)
        await send_text(update, context, "Процесс остановлен")
        return

    if query.startswith("photo:"):
        key = query.split("photo:", 1)[1]
        await cq.edit_message_reply_markup(reply_markup=None)

        try:
            await send_photo(update, context, key)
        except Exception:
            await send_text(update, context, f"⚠️ Такой картинки нет: {key}")
        return

    await send_text(update, context, f"Неизвестная команда: {query}")

async def date_button(update, context):
    cq = update.callback_query
    await cq.answer()
    query = cq.data

    if query == "date_make_profile":
        clear_user_date(context)
        context.chat_data[KEY_DATE_PROFILE] = True
        first_question = FORM_QUESTIONS_OPENER["name"]
        await send_text(update, context, first_question)
    else:
        chatgpt = context.application.bot_data["chatgpt"]
        await send_photo(update,context,query)
        await send_html(update,context,"Отличный выбор! Пригласите собеседника за 5 сообщений на свидание.")
        prompt = load_prompt(query)
        chatgpt.set_prompt(prompt)

async def message_button(update, context):
    cq = update.callback_query
    await cq.answer()
    query = cq.data

    prompt = load_prompt(query)
    history = context.chat_data.get(KEY_DIALOG_LIST, [])
    user_chat_history="\n\n".join(history)
    load_text = "ChatGPT 🤖 думает над вариантами ответов ..."
    await answer_with_loading(update, context, prompt, user_chat_history, load_text)