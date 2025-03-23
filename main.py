from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

PHOTO_BOT_TOKEN = "8149033383:AAENTaj8J7GQq2bY_ceBl2j9L0eHS83859c"
DESTINATION_CHAT_ID = -4703516485  # Replace with your private group/channel ID
TOPIC_ID = 506

async def handle_media_from_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if update.message.message_thread_id != TOPIC_ID:
        return

    user = update.effective_user
    caption = update.message.caption or ""
    sender_info = f"📸 From: @{user.username or user.full_name}\n📝 {caption}"

    # Handle photo
    if update.message.photo:
        photo = update.message.photo[-1].file_id
        sent = await context.bot.send_photo(
            chat_id=DESTINATION_CHAT_ID,
            photo=photo,
            caption=sender_info
        )

    # Handle video
    elif update.message.video:
        video = update.message.video.file_id
        sent = await context.bot.send_video(
            chat_id=DESTINATION_CHAT_ID,
            video=video,
            caption=sender_info
        )

    if sent:
        try:
            await update.message.delete()
        except Exception as e:
            print(f"⚠️ Failed to delete message: {e}")

app = ApplicationBuilder().token(PHOTO_BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ChatType.GROUPS & (filters.PHOTO | filters.VIDEO), handle_media_from_group))
app.run_polling()
