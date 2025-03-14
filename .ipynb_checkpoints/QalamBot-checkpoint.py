#!/usr/bin/env python
# coding: utf-8

# In[1]:


import logging

# Set up logging at the beginning of your script
logging.basicConfig(filename='bot.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Then, you can log something
logging.debug("Bot has started")


# In[2]:


#import all necessary libraries 

import logging
import language_tool_python
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import nest_asyncio
import nltk
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn
import pytz
from datetime import datetime
from telegram import Bot
import nest_asyncio


# In[3]:


# Apply nest_asyncio to avoid event loop conflicts in Jupyter Notebook
nest_asyncio.apply()


# In[4]:


# download necessary NLTK data
nltk.download('wordnet')


# In[5]:


#bot token and username.
Token: Final='7690158589:AAESSAxYHDHipEjmhqr5QhwegVD8gTQrQtM'
BOT_USERNAME:Final = "@QalamAI_Bot"


# In[6]:


# Initialize LanguageTool for grammar checking
tool = language_tool_python.LanguageTool('en-US')


# In[7]:


def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if hasattr(update, 'message'):  # Check if it's an Update object
        logging.info(f"User {update.message.from_user.username} sent: {update.message.text}")



# In[8]:


async def start_command (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_command(update, context)  # Now the function exists
    await update.message.reply_text("👋 Hello! I'm Qalam, your English assistant bot. I can:\n"
        "📖 Correct grammar errors → Use /correct [sentence]\n"
        "📚 Define words → Use /vocabinfo [word]\n"
        "🆘 Need help? Type /help")


# In[9]:


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


# In[10]:


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


# In[11]:


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


# In[12]:


async def reset_command(update: Update, context: ContextTypes):
    log_command( update, context)
    context.user_data.clear()  # Clears stored user data
    await update.message.reply_text("🔄 Session has been reset. You can start fresh now!")


# In[13]:


async def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hi there! How can I help you today?'

    if 'how are you' in processed:
        return "I'm good"

    if 'I love Python' in processed:
        return 'Remember to subscribe'

    return "I'm not sure how to respond to that. Could you try again?"


# In[14]:


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()  # Convert to lowercase for consistency
    
    if "check grammar" in user_message or "correct this" in user_message:
        response = check_grammar(user_message)  # Call your grammar function
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("I'm not sure, sorry...")


# In[15]:


async def process_message(message_type: str, text: str, BOT_USERNAME: str) -> str:
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = await handle_response(new_text)  # Await handle_response
        else:
            return ''  # Return empty if no bot mention
    else:
        response = await handle_response(text)  # Await handle_response for normal messages

    return response


# In[16]:


# Set bot's timezone
timezone = pytz.timezone('Asia/Riyadh')
dt = datetime.now(timezone)


# In[17]:


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")
if __name__=='__main__':
    logging.info('Starting bot...')
# Initialize bot application
    app= Application.builder().token(Token).build()
    #add command handler
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('correct', correct_command))
    app.add_handler(CommandHandler('vocabinfo', vocabinfo_command))
    app.add_handler(CommandHandler('reset', reset_command))

    #add message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message)) 
 
    #add error handler
    app.add_error_handler(error)
    
    nest_asyncio.apply()


async def run_bot():
    logging.info('Polling...')
    await app.run_polling(poll_interval=3)

# Start the bot
asyncio.create_task(run_bot())
print("Running bot...")




# In[ ]:




