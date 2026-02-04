#bot.py

import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from telegram.error import TelegramError

from config import BOT_TOKEN, OPEN_AI_TOKEN
from dialog_state import MODE_PROFILE, MODE_OPENER, MODE_MESSAGE, MODE_DATE, MODE_GPT
from util.gpt import ChatGptService
from handlers.commands import start, gpt, date, message, profile, opener
from handlers.messages import hello
from handlers.callbacks import hello_button, date_button, message_button

# искал ошибку - добавил логирование телеграмм-бота
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

#Это чтобы мы не падали
async def on_error(update, context):
    log.exception("Unhandled error", exc_info=context.error)
    try:
        if update and update.effective_chat:
            await context.bot.send_message(update.effective_chat.id, "⚠️ Упс, ошибка. Попробуй ещё раз.")
    except TelegramError:
        pass

def create_app(bot_token=BOT_TOKEN, open_ai_token=OPEN_AI_TOKEN):
    app = ApplicationBuilder().token(bot_token).build()
    app.bot_data["chatgpt"] = ChatGptService(token=open_ai_token)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(MODE_GPT, gpt))
    app.add_handler(CommandHandler(MODE_DATE, date))
    app.add_handler(CommandHandler(MODE_MESSAGE, message))
    app.add_handler(CommandHandler(MODE_PROFILE, profile))
    app.add_handler(CommandHandler(MODE_OPENER, opener))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

    app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
    app.add_handler(CallbackQueryHandler(message_button, pattern="^message_.*"))
    app.add_handler(CallbackQueryHandler(hello_button))

    app.add_error_handler(on_error)

    return app

def main():
    app = create_app()
    app.run_polling()

if __name__ == "__main__":
    main()
