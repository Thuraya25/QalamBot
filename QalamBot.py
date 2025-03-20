import logging
import os
import asyncio
import nest_asyncio
import nltk
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import language_tool_python
from nltk.corpus import wordnet




# set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for detailed logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("C:\\Users\\thura\\QalamBot\\bot.log"),
        logging.StreamHandler()  # This sends logs to the console
    ]
)

logger = logging.getLogger(__name__)
logger.info("Bot is starting...")


# Apply nest_asyncio for async compatibility
nest_asyncio.apply()


# Initialize NLTK
nltk.download(['punkt', 'wordnet', 'omw-1.4'], quiet=True)


# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')


# Initialize grammar checker
grammar_tool = language_tool_python.LanguageTool('en-US')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received command: {update.message.text}")
    """Handle /start command"""
    await update.message.reply_text("""👋 Hello! I'm Qalam, your English assistant bot. I can:\n
📖 Correct grammar errors → Use /correct [sentence]\n
📚 Define words → Use /define [word]\n
🆘 Need help? Type /help
"""
       
    )


async def correct_grammar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received command: {update.message.text}")
    """Handle /correct command"""
    try:
        text = ' '.join(context.args)
        if not text:
            await update.message.reply_text("Please provide text after /correct")
            return


        matches = grammar_tool.check(text)
        if matches:
            corrected = grammar_tool.correct(text)
            response = f"📝 Corrected text:\n{corrected}"
        else:
            response = "✅ No grammar errors found!"
       
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Grammar correction error: {e}")
        await update.message.reply_text("⚠️ Error processing your request")


async def define_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received command: {update.message.text}")
    """Handle /define command with synonyms"""
    try:
        word = ' '.join(context.args).lower()
        if not word:
            await update.message.reply_text("Please provide a word after /define")
            return


        synsets = wordnet.synsets(word)
        if not synsets:
            await update.message.reply_text(f"❌ No definition found for '{word}'")
            return


        # Get the first three synsets (different meanings)
        response = f"📚 **{word.capitalize()}**\n\n"
       
        for i, synset in enumerate(synsets[:3], 1):
            # Definition
            definition = synset.definition()
            response += f"**Meaning {i}:** {definition}\n"
           
            # Examples
            examples = synset.examples()[:2]
            if examples:
                response += f"🔹 *Examples:*\n- " + "\n- ".join(examples) + "\n"
           
            # Synonyms handling
            lemmas = [lemma.name().replace('_', ' ') for lemma in synset.lemmas()]
            unique_synonyms = list(set([lem for lem in lemmas if lem != word]))
           
            if unique_synonyms:
                response += f"🔸 *Synonyms:* {', '.join(unique_synonyms)}\n\n"
            else:
                response += "🔸 *No distinct synonyms found*\n\n"
       
        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
       
    except Exception as e:
        logger.error(f"Word definition error: {e}")
        await update.message.reply_text("⚠️ Error fetching word information")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received command: {update.message.text}")
    """Handle /help command"""
    help_text = (
        "ℹ️ **Qalam Bot Help**\n\n"
        "/start - Start conversation\n"
        "/correct <text> - Check grammar\n"
        "/define <word> - Get word definition, examples, and synonyms\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all non-command messages"""
    text = update.message.text
    logger.info(f"Received message: {text}")
   
    # Auto-correct functionality
    matches = grammar_tool.check(text)
    if matches:
        corrected = grammar_tool.correct(text)
        await update.message.reply_text(
            f"🤖 I noticed some improvements:\n\n{corrected}",
            parse_mode=ParseMode.MARKDOWN
        )


async def error_handler(update, context):
    try:
        if update and update.message:
            print(f"Update {update} caused error: {context.error}")
        else:
            print(f"An error occurred: {context.error}")
    except Exception as e:
        print(f"Error handling the error: {e}")



def main():
    """Start the bot"""
    try:
        app = Application.builder().token(TOKEN).build()


        # Command handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("correct", correct_grammar))
        app.add_handler(CommandHandler("define", define_word))
        app.add_handler(CommandHandler("help", help_command))
       
        # Message handler
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
       
        # Error handler
        app.add_error_handler(error_handler)


        logger.info("Starting Qalam bot...")
        app.run_polling(drop_pending_updates=True)
       
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")


if __name__ == "__main__":
    main()
