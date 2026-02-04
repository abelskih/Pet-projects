import pytest
from unittest.mock import AsyncMock, MagicMock

import handlers.callbacks as callbacks


def make_context():
    context = MagicMock()
    context.chat_data = {}
    context.application.bot_data = {}
    return context


@pytest.mark.asyncio
async def test_hello_button_start(monkeypatch):
    update = MagicMock()
    update.callback_query.data = "start"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_reply_markup = AsyncMock()
    context = make_context()

    send_text = AsyncMock()
    send_text_buttons = AsyncMock()
    monkeypatch.setattr(callbacks, "send_text", send_text)
    monkeypatch.setattr(callbacks, "send_text_buttons", send_text_buttons)

    await callbacks.hello_button(update, context)

    update.callback_query.edit_message_reply_markup.assert_awaited_once_with(reply_markup=None)
    send_text.assert_awaited_once()
    send_text_buttons.assert_awaited_once()


@pytest.mark.asyncio
async def test_hello_button_photo_error(monkeypatch):
    update = MagicMock()
    update.callback_query.data = "photo:missing"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_reply_markup = AsyncMock()
    context = make_context()

    send_photo = AsyncMock(side_effect=Exception("nope"))
    send_text = AsyncMock()
    monkeypatch.setattr(callbacks, "send_photo", send_photo)
    monkeypatch.setattr(callbacks, "send_text", send_text)

    await callbacks.hello_button(update, context)

    send_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_date_button_make_profile(monkeypatch):
    update = MagicMock()
    update.callback_query.data = "date_make_profile"
    update.callback_query.answer = AsyncMock()
    context = make_context()

    clear_user_date = MagicMock()
    send_text = AsyncMock()
    monkeypatch.setattr(callbacks, "clear_user_date", clear_user_date)
    monkeypatch.setattr(callbacks, "send_text", send_text)

    await callbacks.date_button(update, context)

    clear_user_date.assert_called_once_with(context)
    assert context.chat_data[callbacks.KEY_DATE_PROFILE] is True
    send_text.assert_awaited_once_with(update, context, callbacks.FORM_QUESTIONS_OPENER["name"])


@pytest.mark.asyncio
async def test_date_button_sets_prompt(monkeypatch):
    update = MagicMock()
    update.callback_query.data = "date_robbie"
    update.callback_query.answer = AsyncMock()
    context = make_context()

    chatgpt = MagicMock()
    chatgpt.set_prompt = MagicMock()
    context.application.bot_data["chatgpt"] = chatgpt

    monkeypatch.setattr(callbacks, "send_photo", AsyncMock())
    monkeypatch.setattr(callbacks, "send_html", AsyncMock())
    monkeypatch.setattr(callbacks, "load_prompt", MagicMock(return_value="prompt"))

    await callbacks.date_button(update, context)

    chatgpt.set_prompt.assert_called_once_with("prompt")


@pytest.mark.asyncio
async def test_message_button_calls_answer_with_loading(monkeypatch):
    update = MagicMock()
    update.callback_query.data = "message_next"
    update.callback_query.answer = AsyncMock()
    context = make_context()
    context.chat_data[callbacks.KEY_DIALOG_LIST] = ["a", "b"]

    answer_with_loading = AsyncMock()
    monkeypatch.setattr(callbacks, "answer_with_loading", answer_with_loading)
    monkeypatch.setattr(callbacks, "load_prompt", MagicMock(return_value="prompt"))

    await callbacks.message_button(update, context)

    answer_with_loading.assert_awaited_once()
    args = answer_with_loading.call_args.args
    assert args[2] == "prompt"
    assert args[3] == "a\n\nb"
