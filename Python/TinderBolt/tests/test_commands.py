import pytest
from unittest.mock import AsyncMock, MagicMock

import handlers.commands as commands
from dialog_state import MODE_GPT, MODE_DATE, MODE_MESSAGE, MODE_PROFILE, MODE_OPENER, MODE_MAIN


def make_context():
    context = MagicMock()
    context.chat_data = {}
    return context


@pytest.mark.asyncio
async def test_start_sets_mode_and_shows_main_menu(monkeypatch):
    update = MagicMock()
    context = make_context()

    show_screen = AsyncMock()
    show_main_menu = AsyncMock()
    monkeypatch.setattr(commands, "show_screen", show_screen)
    monkeypatch.setattr(commands, "show_main_menu", show_main_menu)

    await commands.start(update, context)

    assert context.chat_data[commands.KEY_MODE] == MODE_MAIN
    show_screen.assert_awaited_once_with(update, context, MODE_MAIN)
    menu_commands = show_main_menu.call_args.args[2]
    assert set(menu_commands.keys()) == {"start", "profile", "opener", "message", "date", "gpt"}


@pytest.mark.asyncio
async def test_gpt_sets_mode_and_shows_screen(monkeypatch):
    update = MagicMock()
    context = make_context()
    show_screen = AsyncMock()
    monkeypatch.setattr(commands, "show_screen", show_screen)

    await commands.gpt(update, context)

    assert context.chat_data[commands.KEY_MODE] == MODE_GPT
    show_screen.assert_awaited_once_with(update, context, MODE_GPT)


@pytest.mark.asyncio
async def test_date_sets_mode_and_sends_buttons(monkeypatch):
    update = MagicMock()
    context = make_context()

    monkeypatch.setattr(commands, "load_message", MagicMock(return_value="text"))
    send_photo = AsyncMock()
    send_text_buttons = AsyncMock()
    monkeypatch.setattr(commands, "send_photo", send_photo)
    monkeypatch.setattr(commands, "send_text_buttons", send_text_buttons)

    await commands.date(update, context)

    assert context.chat_data[commands.KEY_MODE] == MODE_DATE
    send_photo.assert_awaited_once_with(update, context, MODE_DATE)
    send_text_buttons.assert_awaited_once()
    buttons = send_text_buttons.call_args.args[3]
    assert set(buttons.keys()) == {
        "date_grande",
        "date_robbie",
        "date_zendaya",
        "date_gosling",
        "date_hardy",
        "date_make_profile",
    }


@pytest.mark.asyncio
async def test_message_sets_mode_and_clears_history(monkeypatch):
    update = MagicMock()
    context = make_context()

    monkeypatch.setattr(commands, "load_message", MagicMock(return_value="text"))
    monkeypatch.setattr(commands, "send_photo", AsyncMock())
    monkeypatch.setattr(commands, "send_text_buttons", AsyncMock())
    clear_history = MagicMock()
    monkeypatch.setattr(commands, "clear_history", clear_history)

    await commands.message(update, context)

    assert context.chat_data[commands.KEY_MODE] == MODE_MESSAGE
    clear_history.assert_called_once_with(context)


@pytest.mark.asyncio
async def test_profile_starts_form(monkeypatch):
    update = MagicMock()
    context = make_context()

    show_screen = AsyncMock()
    send_text = AsyncMock()
    clear_user_date = MagicMock()
    monkeypatch.setattr(commands, "show_screen", show_screen)
    monkeypatch.setattr(commands, "send_text", send_text)
    monkeypatch.setattr(commands, "clear_user_date", clear_user_date)

    await commands.profile(update, context)

    assert context.chat_data[commands.KEY_MODE] == MODE_PROFILE
    show_screen.assert_awaited_once_with(update, context, MODE_PROFILE)
    clear_user_date.assert_called_once_with(context)
    send_text.assert_awaited_once_with(update, context, commands.FORM_QUESTIONS["age"])


@pytest.mark.asyncio
async def test_opener_starts_form(monkeypatch):
    update = MagicMock()
    context = make_context()

    show_screen = AsyncMock()
    send_text = AsyncMock()
    clear_user_date = MagicMock()
    monkeypatch.setattr(commands, "show_screen", show_screen)
    monkeypatch.setattr(commands, "send_text", send_text)
    monkeypatch.setattr(commands, "clear_user_date", clear_user_date)

    await commands.opener(update, context)

    assert context.chat_data[commands.KEY_MODE] == MODE_OPENER
    show_screen.assert_awaited_once_with(update, context, MODE_OPENER)
    clear_user_date.assert_called_once_with(context)
    send_text.assert_awaited_once_with(update, context, commands.FORM_QUESTIONS_OPENER["name"])
