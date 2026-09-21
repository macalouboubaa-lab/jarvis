import io
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from config import settings
from agent.core import ask_jarvis

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if settings.TELEGRAM_ALLOWED_USER_ID and user_id != settings.TELEGRAM_ALLOWED_USER_ID:
        await update.message.reply_text("Accès refusé. Instance Jarvis souveraine.")
        return
    await update.message.reply_text("Bonjour Monsieur. Je suis Jarvis, votre assistant personnel souverain.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if settings.TELEGRAM_ALLOWED_USER_ID and user_id != settings.TELEGRAM_ALLOWED_USER_ID:
        return
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    reply = await ask_jarvis(
        update.message.text,
        user_id=str(settings.TELEGRAM_ALLOWED_USER_ID),
    )
    await update.message.reply_text(reply)

def run_bot():
    if not settings.TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN manquant.")
        return
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    print("Bot Telegram démarré.")
    app.run_polling()

if __name__ == "__main__":
    run_bot()
