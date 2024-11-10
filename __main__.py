import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from modules.qr import add_qr_handlers  # Import QR handlers from the modules folder
from modules.translate import add_translate_handlers  # Import translate handlers
from modules.dictionary import add_dictionary_handlers  # Import dictionary handlers
from modules.shortener import add_shortener_handlers  # Import shortener handlers
from config import TOKEN  # Import the bot token from config.py
# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Start command (show all options immediately)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("QR Code", callback_data='qr'),
            InlineKeyboardButton("Translate", callback_data='translate'),
            InlineKeyboardButton("Dictionary", callback_data='dictionary')
        ],
        [
            InlineKeyboardButton("URL Shortener", callback_data='shortener'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the start message with the options
    await update.message.reply_text(
        text="Welcome! Please select an option from the menu:",
        reply_markup=reply_markup
    )

# Callback query handler for the buttons
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    # Check which button was pressed
    if query.data == 'qr':
        await query.edit_message_text(
            text="To generate a QR code, use the /qr command followed by the text or URL. Example:\n"
                 "/qr https://www.example.com"
        )
    elif query.data == 'translate':
        await query.edit_message_text(
            text="To translate text, use the /translate command followed by the language code and the text. Example:\n"
                 "/translate en こんにちは"
        )
    elif query.data == 'dictionary':
        await query.edit_message_text(
            text="To define a word, use the /define command followed by the word you want to look up. Example:\n"
                 "/define hello"
        )
    elif query.data == 'shortener':
        await query.edit_message_text(
            text="To shorten a URL, use the /shorten command followed by the URL. Example:\n"
                 "/shorten https://www.example.com"
        )

# Main entry point
if __name__ == '__main__':
    # Initialize the application with the token from config.py
    application = ApplicationBuilder().token(TOKEN).build()

    # Define handlers
    start_handler = CommandHandler('start', start)
    button_handler = CallbackQueryHandler(button)  # Handle button presses

    # Add handlers to the application
    application.add_handler(start_handler)
    application.add_handler(button_handler)  # Add handler for callback query (button)

    # Register QR, Translate, Dictionary, Shortener, and Weather handlers
    add_qr_handlers(application)  # Handle /qr
    add_translate_handlers(application)  # Handle /translate
    add_dictionary_handlers(application)  # Handle /define
    add_shortener_handlers(application)  # Handle /shorten

    # Run the bot
    application.run_polling()
