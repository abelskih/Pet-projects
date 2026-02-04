import pytest
from unittest.mock import AsyncMock, MagicMock

import state_helpers


def make_context():
    context = MagicMock()
    context.chat_data = {}
    return context


def test_get_user_date_creates_and_reuses():
    context = make_context()
    user1 = state_helpers.get_user_date(context)
    user2 = state_helpers.get_user_date(context)
    assert user1 is user2
    assert context.chat_data["user_date"] is user1


def test_append_to_history_creates_list():
    context = make_context()
    state_helpers.append_to_history(context, "hi")
    state_helpers.append_to_history(context, "there")
    assert context.chat_data["dialog_list"] == ["hi", "there"]


def test_clear_history_and_user_date():
    context = make_context()
    context.chat_data["dialog_list"] = ["a"]
    context.chat_data["user_date"] = {"x": "y"}
    state_helpers.clear_history(context)
    state_helpers.clear_user_date(context)
    assert context.chat_data["dialog_list"] == []
    assert context.chat_data["user_date"] == {}


@pytest.mark.asyncio
async def test_run_form_step_progresses_to_next_question(monkeypatch):
    update = MagicMock()
    update.message.text = "18"
    context = make_context()

    send_text = AsyncMock()
    monkeypatch.setattr(state_helpers, "send_text", send_text)

    store = {}
    steps = [("age", "How old?"), ("city", "Where?")]
    questions = {"age": "How old?", "city": "Where?"}

    result = await state_helpers.run_form_step(
        update,
        context,
        store=store,
        steps=steps,
        questions=questions,
    )

    assert result is None
    assert store == {"age": "18"}
    send_text.assert_awaited_once_with(update, context, "Where?")


@pytest.mark.asyncio
async def test_run_form_step_completes_and_returns_payload(monkeypatch):
    update = MagicMock()
    update.message.text = "Berlin"
    context = make_context()

    send_text = AsyncMock()
    monkeypatch.setattr(state_helpers, "send_text", send_text)
    monkeypatch.setattr(state_helpers, "dialog_user_info_to_str", lambda u: "payload")

    store = {"age": "18"}
    steps = [("age", "How old?"), ("city", "Where?")]
    questions = {"age": "How old?", "city": "Where?"}

    result = await state_helpers.run_form_step(
        update,
        context,
        store=store,
        steps=steps,
        questions=questions,
        done_title_text="Done",
    )

    assert result == "payload"
    assert store == {"age": "18", "city": "Berlin"}
    send_text.assert_awaited_once_with(update, context, "Done")
