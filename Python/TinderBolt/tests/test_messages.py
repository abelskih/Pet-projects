import pytest
from unittest.mock import AsyncMock, MagicMock

import handlers.messages as messages
from dialog_state import MODE_GPT, MODE_DATE, MODE_MESSAGE, MODE_PROFILE, MODE_OPENER


def make_context():
    context = MagicMock()
    context.chat_data = {}
    context.application.bot_data = {}
    return context


@pytest.mark.asyncio
async def test_gpt_dialog_sends_answer(monkeypatch):
    update = MagicMock()
    update.message.text = "hi"
    context = make_context()

    chatgpt = MagicMock()
    chatgpt.send_question = AsyncMock(return_value="answer")
    context.application.bot_data["chatgpt"] = chatgpt

    monkeypatch.setattr(messages, "load_prompt", MagicMock(return_value="prompt"))
    send_text = AsyncMock()
    monkeypatch.setattr(messages, "send_text", send_text)

    await messages.gpt_dialog(update, context)

    chatgpt.send_question.assert_awaited_once_with("prompt", "hi")
    send_text.assert_awaited_once_with(update, context, "answer")


@pytest.mark.asyncio
async def test_date_dialog_profile_mode_routes(monkeypatch):
    update = MagicMock()
    context = make_context()
    context.chat_data[messages.KEY_DATE_PROFILE] = True

    date_profile_form_step = AsyncMock()
    monkeypatch.setattr(messages, "date_profile_form_step", date_profile_form_step)

    await messages.date_dialog(update, context)

    date_profile_form_step.assert_awaited_once_with(update, context)


@pytest.mark.asyncio
async def test_date_dialog_regular_flow(monkeypatch):
    update = MagicMock()
    update.message.text = "hello"
    context = make_context()
    context.chat_data[messages.KEY_DATE_PROFILE] = False

    chatgpt = MagicMock()
    chatgpt.add_message = AsyncMock(return_value="answer")
    context.application.bot_data["chatgpt"] = chatgpt

    my_message = MagicMock()
    my_message.edit_text = AsyncMock()
    send_text = AsyncMock(return_value=my_message)
    monkeypatch.setattr(messages, "send_text", send_text)

    await messages.date_dialog(update, context)

    chatgpt.add_message.assert_awaited_once_with("hello")
    my_message.edit_text.assert_awaited_once_with("answer")


@pytest.mark.asyncio
async def test_hello_routes_by_mode(monkeypatch):
    update = MagicMock()
    update.message.text = "hi"
    context = make_context()

    gpt_dialog = AsyncMock()
    monkeypatch.setattr(messages, "gpt_dialog", gpt_dialog)
    monkeypatch.setattr(messages, "date_dialog", AsyncMock())
    monkeypatch.setattr(messages, "message_dialog", AsyncMock())
    monkeypatch.setattr(messages, "profile_dialog", AsyncMock())
    monkeypatch.setattr(messages, "opener_dialog", AsyncMock())

    context.chat_data[messages.KEY_MODE] = MODE_GPT
    await messages.hello(update, context)

    gpt_dialog.assert_awaited_once_with(update, context)


@pytest.mark.asyncio
async def test_hello_default_flow(monkeypatch):
    update = MagicMock()
    update.message.text = "hi"
    context = make_context()
    context.chat_data[messages.KEY_MODE] = "unknown"

    send_text = AsyncMock()
    send_photo = AsyncMock()
    send_text_buttons = AsyncMock()
    monkeypatch.setattr(messages, "send_text", send_text)
    monkeypatch.setattr(messages, "send_photo", send_photo)
    monkeypatch.setattr(messages, "send_text_buttons", send_text_buttons)

    await messages.hello(update, context)

    assert send_text.await_count == 3
    send_photo.assert_awaited_once()
    send_text_buttons.assert_awaited_once()
