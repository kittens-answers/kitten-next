import logging
from telegram import MenuButtonWebApp, Update, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from answers.settings import BaseSettings

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


class TGSettings(BaseSettings):
    token: str
    menu_url: str


tg_settings = TGSettings()  # type: ignore


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.effective_chat
    await context.bot.setChatMenuButton(
        chat_id=update.effective_chat.id,
        menu_button=MenuButtonWebApp(text="menu", web_app=WebAppInfo(url=tg_settings.menu_url)),
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


if __name__ == "__main__":
    application = ApplicationBuilder().token(tg_settings.token).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
