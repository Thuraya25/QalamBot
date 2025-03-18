#!/usr/bin/env python
# coding: utf-8

# In[2]:


#import all necessary libraries 

import logging
import os
import language_tool_python
from typing import Final
from dotenv import load_dotenv
from telegram import Update
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import CallbackContext
import language_tool_python
import asyncio
import nest_asyncio
import nltk
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn
from nltk.corpus import words
from nltk.corpus import stopwords
import pytz
from datetime import datetime
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download('wordnet')
nltk.download("averaged_perceptron_tagger")


# In[3]:


# Enable logging
logging.basicConfig(filename='bot.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Then, log something
logging.debug("Bot has started")


# In[16]:


# Load Environment Variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")



# In[24]:


nltk.data.path = [r'C:\Users\thura\QalamBot\nltk_data']
nltk.data.path.append(r"C:\Users\thura\QalamBot\nltk_data")  # Add custom NLTK data path


# In[25]:



# In[26]:


# Load the stopwords corpus
stop_words = stopwords.words('english')
print(stop_words[:10])  # Print the first 10 stopwords


# In[27]:


# Get a list of English words
english_words = words.words()
print(english_words[:10])  # Print the first 10 words


# In[28]:


# Load some wordnet synsets in English
synsets = wn.synsets("dog")
print(synsets)

# Use stopwords corpus
stop_words = stopwords.words('english')
print(stop_words[:10])  # First 10 stopwords



# In[29]:


# Initialize LanguageTool for grammar checking
tool = language_tool_python.LanguageTool('en-US')


# In[30]:


def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if hasattr(update, 'message'):  # Check if it's an Update object
        logging.info(f"User {update.message.from_user.username} sent: {update.message.text}")



# In[31]:


async def start_command (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_command(update, context)  # Now the function exists
    await update.message.reply_text("👋 Hello! I'm Qalam, your English assistant bot. I can:\n"
        "📖 Correct grammar errors → Use /correct [sentence]\n"
        "📚 Define words → Use /vocabinfo [word]\n"
        "🆘 Need help? Type /help")


# In[32]:


async def help_command(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    log_command(update, context)
    await update.message.reply_text( "ℹ️ **How to use this bot:**\n\n"
        "✅ **Grammar Correction:**\n"
        "Type: `/correct He are a boy`\n"
        "Response: `He is a boy.`\n\n"
        "✅ **Word Definition:**\n"
        "Type: `/vocabinfo happy`\n"
        "Response: Meaning and synonyms.\n\n"
        "✅ **Reset:**\n"
        "Type: `/reset` to clear session data.\n\n"
        "Need further assistance? Just ask!")


# In[33]:


async def correct_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks and corrects grammar mistakes."""
    log_command(update, context)
    user_input = ' '.join(context.args).strip().lower()
    
    if not user_input:
        await update.message.reply_text("❗ Please provide a sentence after /correct.")
        return
    
    matches = tool.check(user_input)
    
    if not matches:
        response = "✅ No grammar mistakes detected."
    else:
        corrected_text = language_tool_python.utils.correct(user_input, matches)
        response = f"✏️ **Correction:** {corrected_text}"
    
    await update.message.reply_text(response)


# In[34]:


async def vocabinfo_command (update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    """Provides definition and synonyms of a word."""
    log_command(update, context)
    user_input = ' '.join(context.args).strip().lower()
    
    if not user_input:
        await update.message.reply_text("🔍 Please provide a word after /vocabinfo.")
        return
    
    synsets = wordnet.synsets(user_input)
    
    if not synsets:
        await update.message.reply_text(f"❌ Sorry, no definition found for '{user_input}'.")
    else:
        definition = synsets[0].definition()
        synonyms = [lemma.name() for lemma in synsets[0].lemmas()]
        
        message = f"📖 **Word:** {user_input.capitalize()}\n"
        message += f"💡 **Definition:** {definition}\n"
        if synonyms:
            message += f"📝 **Synonyms:** {', '.join(synonyms)}"
        
        await update.message.reply_text(message, parse_mode='Markdown')


# In[35]:


async def reset_command(update: Update, context: ContextTypes):
    log_command( update, context)
    context.user_data.clear()  # Clears stored user data
    await update.message.reply_text("🔄 Session has been reset. You can start fresh now!")


# In[36]:


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



# In[37]:


# Set bot's timezone
timezone = pytz.timezone('Asia/Riyadh')
dt = datetime.now(timezone)


# In[38]:


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")
async def run_bot():
    logging.info("Starting bot...")

    # Initialize bot application
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("correct", correct_command))
    app.add_handler(CommandHandler("vocabinfo", vocabinfo_command))
    app.add_handler(CommandHandler("reset", reset_command))

    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Add error handler
    app.add_error_handler(error)

    nest_asyncio.apply()  # Apply nest_asyncio to prevent event loop issues

    logging.info("Polling started...")
    await app.run_polling(poll_interval=3)

if __name__ == "__main__":
    asyncio.run(run_bot())