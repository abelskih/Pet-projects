from typing import Optional

from dialog_state import KEY_DIALOG_LIST, KEY_USER_DATE
from util.util import load_message, send_photo, send_text, dialog_user_info_to_str


def get_user_date(context) -> dict:
    user = context.chat_data.get(KEY_USER_DATE)
    if user is None:
        user = {}
        context.chat_data[KEY_USER_DATE] = user
    return user

def append_to_history(context, text: str):
    history = context.chat_data.get(KEY_DIALOG_LIST)
    if history is None:
        history = []
        context.chat_data[KEY_DIALOG_LIST] = history
    history.append(text)

def clear_history(context):
    context.chat_data[KEY_DIALOG_LIST] = []

def clear_user_date(context):
    context.chat_data[KEY_USER_DATE] = {}

async def show_screen(update, context, mode: str):
    text = load_message(mode)
    await send_photo(update, context, mode)
    await send_text(update, context, text)

async def answer_with_loading(update, context, prompt: str, payload: str, load_message: str):
    chatgpt = context.application.bot_data["chatgpt"]
    my_message = await send_text(update, context, load_message)
    answer = await chatgpt.send_question(prompt, payload)
    await my_message.edit_text(answer)
    return answer

async def run_form_step(
    update,
    context,
    *,
    store: dict,
    steps: list,
    questions: dict,
    done_title_text: str = "Анкета заполнена ✅",
    already_done_text: str = "Анкета уже заполнена 🙂",
) -> Optional[str]:
    text = update.message.text
    step = len(store)
    if step >= len(steps):
        await send_text(update, context, already_done_text)
        return None

    field, _ = steps[step]
    store[field] = text
    step += 1

    if step < len(steps):
        next_field, _ = steps[step]
        next_question = questions[next_field]
        await send_text(update, context, next_question)
        return None

    await send_text(update, context, done_title_text)
    payload = dialog_user_info_to_str(store)
    return payload