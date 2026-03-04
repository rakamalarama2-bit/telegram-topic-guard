import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

POLICY_TOPIC_ID = 6
HOWTOPLAY_TOPIC_ID = 12
ANNOUNCEMENT_TOPIC_ID = 19


async def lock_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    chat_id = message.chat_id
    thread_id = message.message_thread_id
    user_id = message.from_user.id

    # Only act inside locked topics
    if thread_id not in [POLICY_TOPIC_ID, HOWTOPLAY_TOPIC_ID, ANNOUNCEMENT_TOPIC_ID]:
        return

    try:
        member = await context.bot.get_chat_member(chat_id, user_id)

        # Allow admins and owner
        if member.status in ["administrator", "creator"]:
            return

        # Delete normal member messages
        await message.delete()

    except Exception as e:
        print("Error:", e)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.ALL & filters.ChatType.SUPERGROUP, lock_topics)
)

print("Topic Guard Bot running...")
app.run_polling()
