from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = "7586827626:AAEqh5F2ybzgOib55I44EFMsErrAoJLg8Ak"
NAME = "Moonophile 🌙"

# Safe limit define karo (Telegram safe max ~100-200 recent messages)
SAFE_LIMIT = 70

async def clean(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Admin check
    member = await context.bot.get_chat_member(chat_id, update.effective_user.id)
    if member.status not in ["administrator", "creator"]:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"❌ Sirf moonophile use kar sakti hai.\n— {NAME}"
        )
        return

    deleted = 0
    start_id = update.message.message_id

    # Delete loop (safe limit)
    for i in range(start_id, start_id - SAFE_LIMIT, -1):
        try:
            await context.bot.delete_message(chat_id, i)
            deleted += 1
            # Small sleep to avoid flood error
            await asyncio.sleep(0.05)
        except:
            pass

    # Cool Moonophile reply
    cool_replies = [
        f"🧹 Clean complete. {deleted} ho gaya mara aaka boliya kya hukm ha 😁!\n— {NAME}",
        f"✨ Group ab saaf! {deleted} messages delete hue.\nMoonophile style 🌙",
        f"💫 Boom! {deleted} messages vanish. — {NAME} lo apka kam ho gay moonophile ji🌙",
        f"🌟 Trash cleared! {deleted} msgs deleted. — {NAME} lo apka kam ho gay moonophile ji "
    ]

    # Random cool reply
    import random
    await context.bot.send_message(
        chat_id=chat_id,
        text=random.choice(cool_replies)
    )

# Setup bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("clean", clean))

print("Moonophile clean bot running...")

# Polling with timeout + safe handling
app.run_polling(
    drop_pending_updates=True,
    poll_interval=2,
    timeout=30
)