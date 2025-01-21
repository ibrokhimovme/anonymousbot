from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import uuid

# Foydalanuvchilarni bog'lash uchun ma'lumotlar bazasi
user_links = {}  # {'user_id': 'link', 'link': 'user_id'}
pending_messages = {}  # {'user_id': 'ref_user_id'}

# Shaxsiy havola yaratish funksiyasi
def generate_personal_link(user_id, bot_username):
    if user_id not in user_links:
        unique_link = str(uuid.uuid4())[:8]  # Unikal havola yaratiladi
        user_links[user_id] = unique_link
        user_links[unique_link] = user_id

    unique_link = user_links[user_id]
    return f"https://t.me/{bot_username}?start={unique_link}"

def create_share_button(link):
    keyboard = [
        [InlineKeyboardButton("Поделиться ссылкой", url=link)]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    args = context.args

    if args:
        ref_link = args[0]
        if ref_link in user_links:
            ref_user_id = user_links[ref_link]
            pending_messages[user_id] = ref_user_id
            await update.message.reply_text("Напиши анонимный вопрос:")
        else:
            await update.message.reply_text("Try again. Link isnt true")
    else:
        # Foydalanuvchi uchun yangi link yaratish
        personal_link = generate_personal_link(user_id, context.bot.username)
        share_link = personal_link[8:]
        await update.message.reply_text(
            f"Твоя ссылкa для вопросов:\n{personal_link}\nПокажи эту ссылку друзьям и подписчикам и получай от них анонимные вопросы и отвечай!",
            reply_markup=create_share_button(f"http://t.me/share/url?url={share_link}")
        )

        # Kanalga foydalanuvchining malumotlarini yuborish
        channel_id = '@daily_codee'  # Bu yerga kanalning usernameni kiriting
        user_info = f"Ism: {update.effective_user.first_name}\nFamiliya: {update.effective_user.last_name if update.effective_user.last_name else 'Not provided'}\nUsername: @{update.effective_user.username if update.effective_user.username else 'Not provided'}"
        
        await context.bot.send_message(channel_id, user_info)

async def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in pending_messages:
        ref_user_id = pending_messages.pop(user_id)
        if update.message.text:
            await context.bot.send_message(chat_id=ref_user_id, text=f"У вас новое сообщение: {update.message.text}")
            await update.message.reply_text("Ваше сообщение успешно отправлено.")
        elif update.message.photo:
            await context.bot.send_photo(chat_id=ref_user_id, photo=update.message.photo[-1].file_id, caption=f"У вас новое сообщение: ")
            await update.message.reply_text("Ваше изображение успешно отправлено.")
        elif update.message.sticker:
            await context.bot.send_sticker(chat_id=ref_user_id, sticker=update.message.sticker.file_id)
            await update.message.reply_text("Ваша sticker успешно отправлена.")
        else:
            await update.message.reply_text("Вы можете отправлять только текст, изображения или наклейки...")

        personal_link = generate_personal_link(user_id, context.bot.username)
        share_link = personal_link[8:]
        await update.message.reply_text(
            f"Твоя ссылкa для вопросов: \n{personal_link} \nПокажи эту ссылку друзьям и подписчикам и получай от них анонимные вопросы и отвечай!",
            reply_markup=create_share_button(f"http://t.me/share/url?url={share_link}")
        )
    else:
        await update.message.reply_text("Чтобы воспользоваться ботом, необходимо сначала ввести команду /start или войти в систему по соответствующей ссылке...")

def main():
    TOKEN = "7791415930:AAE4AWPbQqdlBgeUa7MHCMkSWCc9Jqis0WE"  # O'zingizning bot tokeningizni kiriting
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()