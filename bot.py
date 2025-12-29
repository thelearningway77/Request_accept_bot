import logging
from telegram import Update, ChatMemberUpdated
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes
from telegram.constants import ChatMemberStatus

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_IDS = [123456789]  # Replace with your Telegram user ID(s)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "👋 Hello! I'm an Auto-Accept Bot.\n\n"
        "Add me to your group and make me an admin with:\n"
        "✅ 'Add Members' permission\n\n"
        "I'll automatically accept all join requests!"
    )

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Automatically approve join requests"""
    chat_member_update = update.chat_join_request
    
    if not chat_member_update:
        return
    
    chat = chat_member_update.chat
    user = chat_member_update.from_user
    
    try:
        # Approve the join request
        await context.bot.approve_chat_join_request(
            chat_id=chat.id,
            user_id=user.id
        )
        
        logger.info(f"✅ Approved join request from {user.first_name} (@{user.username}) in {chat.title}")
        
        # Optional: Send welcome message to the user
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text=f"✅ Your request to join '{chat.title}' has been approved!\n\nWelcome! 🎉"
            )
        except Exception as e:
            logger.warning(f"Could not send welcome message to user: {e}")
        
        # Optional: Notify admins
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=f"✅ Auto-approved join request:\n\n"
                         f"User: {user.first_name} (@{user.username or 'N/A'})\n"
                         f"User ID: {user.id}\n"
                         f"Group: {chat.title}"
                )
            except Exception as e:
                logger.error(f"Error notifying admin {admin_id}: {e}")
        
    except Exception as e:
        logger.error(f"Error approving join request: {e}")
        
        # Notify admins of error
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=f"❌ Failed to approve join request:\n\n"
                         f"User: {user.first_name} (@{user.username or 'N/A'})\n"
                         f"Group: {chat.title}\n"
                         f"Error: {str(e)}"
                )
            except:
                pass

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot stats (admin only)"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Admin only command!")
        return
    
    await update.message.reply_text(
        "📊 Bot Statistics\n\n"
        "The bot is running and monitoring join requests.\n\n"
        "Make sure the bot is added to your group with admin rights!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    await update.message.reply_text(
        "🤖 Auto-Accept Bot Help\n\n"
        "**Setup Instructions:**\n"
        "1. Add me to your group\n"
        "2. Make me an admin\n"
        "3. Give me 'Invite Users via Link' permission\n"
        "4. Enable 'Approve New Members' in group settings\n\n"
        "That's it! I'll auto-approve all join requests.\n\n"
        "**Commands:**\n"
        "/start - Start the bot\n"
        "/help - Show this message\n"
        "/stats - Bot statistics (admin only)"
    )

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats))
    
    # Handle join requests
    application.add_handler(ChatMemberHandler(handle_join_request, ChatMemberHandler.CHAT_JOIN_REQUEST))
    
    # Start bot
    logger.info("🤖 Auto-Accept Bot started!")
    logger.info("Monitoring join requests...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
