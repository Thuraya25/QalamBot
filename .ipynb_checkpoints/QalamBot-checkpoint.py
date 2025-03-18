import logging
import os
import requests
import nltk
from nltk.corpus import wordnet as wn
import asyncio
import nest_asyncio
import language_tool_python

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load Environment Variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Initialize LanguageTool for grammar checking
tool = language_tool_python.LanguageTool('en-US')


# Download necessary NLP resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")
nltk.download("words")

# Define bot commands
async def start_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("\U0001F44B Hello! I'm Qalam, your English assistant bot. I can:\n"
        "\U0001F4D6 Correct grammar errors → Use /correct [sentence]\n"
        "\U0001F4DA Define words → Use /vocabinfo [word]\n"
        "\U0001F198 Need help? Type /help"
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("\u2139\uFE0F **How to use this bot:**\n\n"
        "\u2705 **Grammar Correction:**\n"
        "Type: `/correct He are a boy`\n"
        "Response: `He is a boy.`\n\n"
        "\u2705 **Word Definition:**\n"
        "Type: `/vocabinfo happy`\n"
        "Response: Meaning and synonyms.\n\n"
        "\u2705 **Reset:**\n"
        "Type: `/reset` to clear session data.\n\n"
        "Need further assistance? Just ask!"
    )

async def vocabinfo_command(update: Update, context: CallbackContext) -> None:
    # Get the word from the command arguments
    word = " ".join(context.args)
    
    if not word:
        await update.message.reply_text("❗ Please provide a word after /vocabinfo. Example: /vocabinfo happy.")
        return

    # Get the synsets of the word (synsets represent the word's meaning in WordNet)
    synsets = wn.synsets(word)

    if not synsets:
        await update.message.reply_text(f"❗ No information found for the word '{word}'.")
        return

    # Get the first synset (most common meaning) for simplicity
    synset = synsets[0]

    # Get the definition of the word
    definition = synset.definition()

    # Get synonyms from the synset's lemmas
    synonyms = set()
    for lemma in synset.lemmas():
        synonyms.add(lemma.name())

    # Format the message to be sent to the user
    response = f"🔍 Word: {word}\n\n"
    response += f"📝 Definition: {definition}\n\n"
    response += "🔄 Synonyms: " + ", ".join(synonyms)

    # Send the response to the user
    await update.message.reply_text(response)


async def correct_command(update: Update, context: CallbackContext):
    user_input = " ".join(context.args)
    if not user_input:
        await update.message.reply_text("❗ Please provide a sentence after /correct. Example: /correct She go to school.")
        return
    
    # Use LanguageTool to check the sentence for mistakes
    matches = tool.check(user_input)

    # If no mistakes are found, inform the user
    if not matches:
        await update.message.reply_text("✅ No mistakes found!")
    else:
        # Apply corrections
        corrected = language_tool_python.utils.correct(user_input, matches)
        await update.message.reply_text(f"Corrected sentence: {corrected}")

async def reset_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Resetting your session...")

# Grammar correction with TextBlob

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text

    # Check if the message starts with a command
    if user_text.startswith('/correct'):
        await update.message.reply_text("❗ Please provide a sentence after /correct. Example: /correct She go to school.")
        return
    elif user_text.startswith('/vocabinfo'):
        await update.message.reply_text("❗ Please provide a word after /vocabinfo. Example: /vocabinfo happy.")
        return

    # Check for grammar issues in the message using LanguageTool
    matches = tool.check(user_text)
    corrected_text = language_tool_python.utils.correct(user_text, matches)

    if user_text.lower() == corrected_text.lower():
        response = "Your sentence looks good! ✅"
    else:
        response = f"Here's a suggestion:\n{corrected_text}"

    # Log the original and corrected text
    logger.info(f"User input: {user_text} | Corrected: {corrected_text}")
    
    # Send the response back to the user
    await update.message.reply_text(response)


    # Log the original and corrected text (if needed for debugging or further analysis)
    logger.info(f"User input: {user_text} | Corrected: {corrected_text}")
    
    # Send the response back to the user
    await update.message.reply_text(response)


    # Log the original and corrected text
    logger.info(f"User input: {user_text} | Corrected: {corrected_text}")
    
    # Send the response back to the user
    update.message.reply_text(response)

# Error Handler
async def error(update: object, context: CallbackContext):
    logger.warning(f"Update {update} caused error {context.error}")


# Main function to start the bot
async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("vocabinfo", vocabinfo_command))
    application.add_handler(CommandHandler("correct", correct_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_error_handler(error)

    # Handle messages (grammar correction)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot with long polling
    await application.run_polling()
    logging.info("Bot is starting...")
    print("Bot is starting...")



if __name__ == "__main__":
    nest_asyncio.apply()  
    asyncio.run(main())