import pytest
from unittest.mock import AsyncMock, MagicMock

import util.util as util


def test_dialog_user_info_to_str_includes_values():
    user = {"name": "Bob", "age": "20", "city": "Paris"}
    result = util.dialog_user_info_to_str(user)
    assert "Bob" in result
    assert "20" in result
    assert "Paris" in result
    assert result.count("\n") >= 2


@pytest.mark.asyncio
async def test_send_text_with_invalid_markdown_uses_reply_text():
    update = MagicMock()
    update.message = MagicMock()
    update.effective_chat.id = 1
    update.message.reply_text = AsyncMock()

    context = MagicMock()
    context.bot.send_message = AsyncMock()

    await util.send_text(update, context, "bad_markdown")

    update.message.reply_text.assert_awaited_once()
    context.bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_send_text_with_valid_markdown_uses_send_message():
    update = MagicMock()
    update.message = MagicMock()
    update.effective_chat.id = 7
    update.message.reply_text = AsyncMock()

    context = MagicMock()
    context.bot.send_message = AsyncMock()

    await util.send_text(update, context, "oktext")

    context.bot.send_message.assert_awaited_once()
    update.message.reply_text.assert_not_awaited()


@pytest.mark.asyncio
async def test_send_text_buttons_uses_callback_query_message():
    update = MagicMock()
    update.callback_query.message.reply_text = AsyncMock()

    context = MagicMock()

    await util.send_text_buttons(update, context, "hi", {"k": "v"})

    update.callback_query.message.reply_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_text_buttons_uses_update_message_when_no_callback():
    update = MagicMock()
    update.callback_query = None
    update.message.reply_text = AsyncMock()

    context = MagicMock()

    await util.send_text_buttons(update, context, "hi", {"k": "v"})

    update.message.reply_text.assert_awaited_once()
