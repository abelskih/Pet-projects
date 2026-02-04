# handlers/messages.py

import logging
from dialog_state import MODE_MESSAGE, FORM_STEPS, MODE_PROFILE, FORM_QUESTIONS, MODE_OPENER, FORM_STEPS_OPENER, \
    FORM_QUESTIONS_OPENER, KEY_DATE_PROFILE
from state_helpers import append_to_history, get_user_date, answer_with_loading, run_form_step
from util.util import send_text, load_prompt, send_photo, send_text_buttons, dialog_user_info_to_str
from handlers.commands import KEY_MODE, MODE_GPT, MODE_DATE

log = logging.getLogger(__name__)

async def gpt_dialog(update, context):
    text = update.message.text
    chatgpt = context.application.bot_data["chatgpt"]
    prompt = load_prompt("gpt")

    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)

async def date_dialog(update, context):
    if context.chat_data.get(KEY_DATE_PROFILE):
        await date_profile_form_step(update, context)
        return
    else:
        text=update.message.text
        chatgpt = context.application.bot_data["chatgpt"]
        my_message = await send_text(update, context, "Набирает текст ...")
        answer = await chatgpt.add_message(text)
        await my_message.edit_text(answer)

async def date_profile_form_step(update, context):
    profile = get_user_date(context)
    payload = await run_form_step(
        update,
        context,
        store=profile,
        steps=FORM_STEPS_OPENER,
        questions=FORM_QUESTIONS_OPENER,
        done_title_text="Профиль для свиданий заполнен ✅",
    )
    if payload is None:
        return

    chatgpt = context.application.bot_data["chatgpt"]
    prompt = load_prompt("date_make_profile") + payload
    chatgpt.set_prompt(prompt)
    context.chat_data[KEY_DATE_PROFILE] = False
    await send_text(update, context, "Готово ✅ Теперь можешь продолжать переписку в режиме свидания 🙂")

async def message_dialog(update, context):
    append_to_history(context, update.message.text)

async def profile_dialog(update, context):
    user=get_user_date(context)
    user_info = await run_form_step(
        update, context,
        store=user,
        steps=FORM_STEPS,
        questions=FORM_QUESTIONS,
        done_title_text="Профиль заполнен ✅",
    )
    if user_info is not None:
        prompt=load_prompt(MODE_PROFILE)
        load_text = "ChatGPT 🤖 занимается генерацией профиля ..."
        await answer_with_loading(update, context, prompt, user_info, load_text)

async def opener_dialog(update, context):
    parent=get_user_date(context)
    parent_info = await run_form_step(
        update, context,
        store=parent,
        steps=FORM_STEPS_OPENER,
        questions=FORM_QUESTIONS_OPENER,
        done_title_text="Профиль заполнен ✅",
    )
    if parent_info is not None:
        prompt=load_prompt(MODE_OPENER)
        load_text = "ChatGPT 🤖 занимается генерацией профиля ..."
        await answer_with_loading(update, context, prompt, parent_info, load_text)


async def hello(update, context):
    if not update.message or not update.message.text:
        return

    mode = context.chat_data.get(KEY_MODE)

    if mode == MODE_GPT:
        await gpt_dialog(update, context)
        return

    if mode == MODE_DATE:
        await date_dialog(update, context)
        return

    if mode == MODE_MESSAGE:
        await message_dialog(update, context)
        return

    if mode == MODE_PROFILE:
        await profile_dialog(update, context)
        return

    if mode == MODE_OPENER:
        await opener_dialog(update, context)
        return

    await send_text(update, context, "*Привет*")
    await send_text(update, context, "_Как дела?_")
    await send_text(update, context, "Вы написали: " + update.message.text)

    await send_photo(update, context, "avatar_main")
    await send_text_buttons(update, context, "Запустить процесс?", {
        "start": "Запустить",
        "stop": "Остановить"
    })