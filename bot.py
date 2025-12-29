import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_IDS = [int(os.environ.get("ADMIN_ID", "123456789"))]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Auto-Accept Bot is ready! Add me to your group as admin.")

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_join = update.chat_join_request
    if not chat_join:
        return
    
    try:
        await context.bot.approve_chat_join_request(chat_id=chat_join.chat.id, user_id=chat_join.from_user.id)
        logger.info(f"Approved: {chat_join.from_user.first_name}")
    except Exception as e:
        logger.error(f"Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(handle_join_request, -1))
    logger.info("Bot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
