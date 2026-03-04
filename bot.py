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
    user = message.from_user
    thread_id = message.message_thread_id

    # Check if user is admin
    member = await context.bot.get_chat_member(chat_id, user.id)

    if member.status in ["administrator", "creator"]:
        return  # allow admins

    # Delete member messages in locked topics
    if thread_id in [POLICY_TOPIC_ID, HOWTOPLAY_TOPIC_ID, ANNOUNCEMENT_TOPIC_ID]:
        try:
            await message.delete()
        except:
            pass


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.ALL & filters.ChatType.SUPERGROUP, lock_topics)
)

print("Topic Guard Bot running...")
app.run_polling()
