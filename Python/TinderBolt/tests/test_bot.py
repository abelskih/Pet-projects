import pytest
from unittest.mock import AsyncMock, MagicMock, ANY

import bot
from telegram.error import TelegramError


def test_create_app_registers_handlers(monkeypatch):
    app = MagicMock()
    app.bot_data = {}

    builder = MagicMock()
    builder.token.return_value = builder
    builder.build.return_value = app
    monkeypatch.setattr(bot, "ApplicationBuilder", MagicMock(return_value=builder))

    chatgpt_sentinel = object()
    chatgpt_cls = MagicMock(return_value=chatgpt_sentinel)
    monkeypatch.setattr(bot, "ChatGptService", chatgpt_cls)

    command_handler = MagicMock(side_effect=lambda *a, **k: ("CommandHandler", a, k))
    message_handler = MagicMock(side_effect=lambda *a, **k: ("MessageHandler", a, k))
    callback_handler = MagicMock(side_effect=lambda *a, **k: ("CallbackQueryHandler", a, k))
    monkeypatch.setattr(bot, "CommandHandler", command_handler)
    monkeypatch.setattr(bot, "MessageHandler", message_handler)
    monkeypatch.setattr(bot, "CallbackQueryHandler", callback_handler)

    result = bot.create_app("BOT", "OPEN")

    assert result is app
    builder.token.assert_called_once_with("BOT")
    chatgpt_cls.assert_called_once_with(token="OPEN")
    assert app.bot_data["chatgpt"] is chatgpt_sentinel

    expected_cmd_calls = [
        (("start", bot.start), {}),
        ((bot.MODE_GPT, bot.gpt), {}),
        ((bot.MODE_DATE, bot.date), {}),
        ((bot.MODE_MESSAGE, bot.message), {}),
        ((bot.MODE_PROFILE, bot.profile), {}),
        ((bot.MODE_OPENER, bot.opener), {}),
    ]
    actual_cmd_calls = [(c.args, c.kwargs) for c in command_handler.call_args_list]
    assert actual_cmd_calls == expected_cmd_calls

    message_handler.assert_called_once()
    assert message_handler.call_args.args[1] is bot.hello

    expected_cb_calls = [
        ((bot.date_button,), {"pattern": "^date_.*"}),
        ((bot.message_button,), {"pattern": "^message_.*"}),
        ((bot.hello_button,), {}),
    ]
    actual_cb_calls = [(c.args, c.kwargs) for c in callback_handler.call_args_list]
    assert actual_cb_calls == expected_cb_calls

    assert app.add_handler.call_count == 10
    app.add_error_handler.assert_called_once_with(bot.on_error)


def test_main_runs_polling(monkeypatch):
    app = MagicMock()
    monkeypatch.setattr(bot, "create_app", MagicMock(return_value=app))

    bot.main()

    app.run_polling.assert_called_once_with()


@pytest.mark.asyncio
async def test_on_error_sends_message():
    update = MagicMock()
    update.effective_chat.id = 123

    context = MagicMock()
    context.error = Exception("boom")
    context.bot.send_message = AsyncMock()

    await bot.on_error(update, context)

    context.bot.send_message.assert_awaited_once_with(123, ANY)


@pytest.mark.asyncio
async def test_on_error_no_update_no_send():
    context = MagicMock()
    context.error = Exception("boom")
    context.bot.send_message = AsyncMock()

    await bot.on_error(None, context)

    context.bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_on_error_telegram_error_swallowed():
    update = MagicMock()
    update.effective_chat.id = 123

    context = MagicMock()
    context.error = Exception("boom")
    context.bot.send_message = AsyncMock(side_effect=TelegramError("fail"))

    await bot.on_error(update, context)
