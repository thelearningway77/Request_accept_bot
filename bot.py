import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(os.getenv("ADMIN_ID", "0"))]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running! Add me to your group.")

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_join_request:
        req = update.chat_join_request
        try:
            await context.bot.approve_chat_join_request(
                chat_id=req.chat.id,
                user_id=req.from_user.id
            )
            logger.info(f"✅ Approved: {req.from_user.first_name}")
        except Exception as e:
            logger.error(f"❌ Error: {e}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(ChatMemberHandler(handle_join_request, ChatMemberHandler.CHAT_JOIN_REQUEST))
    
    logger.info("🤖 Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
