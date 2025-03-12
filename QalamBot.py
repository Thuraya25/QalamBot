#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import logging
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import language_tool_python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger') 

# Load environment variables
load_dotenv()
telegram_token = os.getenv('TELEGRAM_TOKEN')
bot_username = os.getenv('BOT_USERNAME')

if not telegram_token:
    raise ValueError("TELEGRAM_TOKEN is missing. Please check your .env file.")

# Enable nest_asyncio to avoid event loop issues
nest_asyncio.apply()

# Initialize logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize LanguageTool
tool = language_tool_python.LanguageTool('en-US')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your grammar assistant bot. Type your message, and I'll help!")

def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.from_user:
        logging.info(f"User {update.message.from_user.username} sent: {update.message.text}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a sentence, and I'll check its grammar!")

async def correct_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    matches = tool.check(user_input)
    corrected_text = tool.correct(user_input)
    await update.message.reply_text(f"Corrected sentence: {corrected_text}")

async def handle_response(user_message: str) -> str:
    return "I'm here to help! Try sending a message."

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command(update, context)
    user_message = update.message.text.lower()

    if "check grammar" in user_message or "correct this" in user_message:
        await correct_command(update, context)
    else:
        response = handle_response(user_message)
        await update.message.reply_text(response)

async def run_bot():
    app = Application.builder().token(telegram_token).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    logging.info("Bot is running...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(run_bot())




# In[ ]:




