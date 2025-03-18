{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "652b4b2d-72d4-4d20-b990-dd82c6932c8c",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[nltk_data] Downloading package punkt to\n",
      "[nltk_data]     C:\\Users\\thura\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Package punkt is already up-to-date!\n",
      "[nltk_data] Downloading package stopwords to\n",
      "[nltk_data]     C:\\Users\\thura\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Package stopwords is already up-to-date!\n",
      "[nltk_data] Downloading package omw-1.4 to\n",
      "[nltk_data]     C:\\Users\\thura\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Package omw-1.4 is already up-to-date!\n",
      "[nltk_data] Downloading package wordnet to\n",
      "[nltk_data]     C:\\Users\\thura\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Package wordnet is already up-to-date!\n",
      "[nltk_data] Downloading package averaged_perceptron_tagger to\n",
      "[nltk_data]     C:\\Users\\thura\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Package averaged_perceptron_tagger is already up-to-\n",
      "[nltk_data]       date!\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#import all necessary libraries \n",
    "\n",
    "import logging\n",
    "import os\n",
    "import language_tool_python\n",
    "from typing import Final\n",
    "from dotenv import load_dotenv\n",
    "from telegram import Update\n",
    "from telegram import Bot\n",
    "from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes\n",
    "from telegram.ext import CallbackContext\n",
    "import language_tool_python\n",
    "import asyncio\n",
    "import nest_asyncio\n",
    "import nltk\n",
    "from nltk.corpus import wordnet\n",
    "from nltk.corpus import wordnet as wn\n",
    "from nltk.corpus import words\n",
    "from nltk.corpus import stopwords\n",
    "import pytz\n",
    "from datetime import datetime\n",
    "nltk.download('punkt')\n",
    "nltk.download('stopwords')\n",
    "nltk.download('omw-1.4')\n",
    "nltk.download('wordnet')\n",
    "nltk.download(\"averaged_perceptron_tagger\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "94f6f354-7719-49b3-bd15-3e37e671bb67",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# Enable logging\n",
    "logging.basicConfig(filename='bot.log', level=logging.DEBUG,\n",
    "                    format='%(asctime)s - %(levelname)s - %(message)s')\n",
    "\n",
    "# Then, log something\n",
    "logging.debug(\"Bot has started\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "c38e3c41-d8fe-4ec4-af01-c48cb8ee7912",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# Load Environment Variables\n",
    "load_dotenv()\n",
    "TELEGRAM_TOKEN = os.getenv(\"TELEGRAM_TOKEN\")\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "d4a72414-5677-4edb-ac19-6098526acd15",
   "metadata": {},
   "outputs": [],
   "source": [
    "nltk.data.path = [r'C:\\Users\\thura\\QalamBot\\nltk_data']\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "5a9e63e2-ca61-4d79-b50c-cffecc2d366e",
   "metadata": {},
   "outputs": [],
   "source": [
    "  # Add custom NLTK data path\n",
    "nltk_data_path = os.path.join(os.getcwd(), \"nltk_data\")\n",
    "nltk.data.path.append(nltk_data_path)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "cf07fd87-0e56-4dce-86e7-92cacdf04f73",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an']\n"
     ]
    }
   ],
   "source": [
    "\n",
    "# Load the stopwords corpus\n",
    "stop_words = stopwords.words('english')\n",
    "print(stop_words[:10])  # Print the first 10 stopwords\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "55464ade-dae6-4c04-ad3c-a1a23518f2c3",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['A', 'a', 'aa', 'aal', 'aalii', 'aam', 'Aani', 'aardvark', 'aardwolf', 'Aaron']\n"
     ]
    }
   ],
   "source": [
    "# Get a list of English words\n",
    "english_words = words.words()\n",
    "print(english_words[:10])  # Print the first 10 words\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "ccb1aa4f-b68f-462e-b45b-98455519065b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[Synset('dog.n.01'), Synset('frump.n.01'), Synset('dog.n.03'), Synset('cad.n.01'), Synset('frank.n.02'), Synset('pawl.n.01'), Synset('andiron.n.01'), Synset('chase.v.01')]\n",
      "['a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an']\n"
     ]
    }
   ],
   "source": [
    "\n",
    "# Load some wordnet synsets in English\n",
    "synsets = wn.synsets(\"dog\")\n",
    "print(synsets)\n",
    "\n",
    "# Use stopwords corpus\n",
    "stop_words = stopwords.words('english')\n",
    "print(stop_words[:10])  # First 10 stopwords\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "2e67b075-7292-4774-b81b-d938dc7181f4",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Initialize LanguageTool for grammar checking\n",
    "tool = language_tool_python.LanguageTool('en-US')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "d31b07eb-c829-4b2b-9524-acb5fbe7f18a",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):\n",
    "    if hasattr(update, 'message'):  # Check if it's an Update object\n",
    "        logging.info(f\"User {update.message.from_user.username} sent: {update.message.text}\")\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "ee4d55e9-8701-420e-8ef4-f3a1e57d666b",
   "metadata": {},
   "outputs": [],
   "source": [
    "async def start_command (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:\n",
    "    log_command(update, context)  # Now the function exists\n",
    "    await update.message.reply_text(\"👋 Hello! I'm Qalam, your English assistant bot. I can:\\n\"\n",
    "        \"📖 Correct grammar errors → Use /correct [sentence]\\n\"\n",
    "        \"📚 Define words → Use /vocabinfo [word]\\n\"\n",
    "        \"🆘 Need help? Type /help\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "604ecc89-14f1-4521-bf50-e447df8aad92",
   "metadata": {},
   "outputs": [],
   "source": [
    "async def help_command(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:\n",
    "    log_command(update, context)\n",
    "    await update.message.reply_text( \"ℹ️ **How to use this bot:**\\n\\n\"\n",
    "        \"✅ **Grammar Correction:**\\n\"\n",
    "        \"Type: `/correct He are a boy`\\n\"\n",
    "        \"Response: `He is a boy.`\\n\\n\"\n",
    "        \"✅ **Word Definition:**\\n\"\n",
    "        \"Type: `/vocabinfo happy`\\n\"\n",
    "        \"Response: Meaning and synonyms.\\n\\n\"\n",
    "        \"✅ **Reset:**\\n\"\n",
    "        \"Type: `/reset` to clear session data.\\n\\n\"\n",
    "        \"Need further assistance? Just ask!\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "10bad6a0-dae4-418d-b4cf-71c1ea6c6a98",
   "metadata": {},
   "outputs": [],
   "source": [
    "async def correct_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:\n",
    "    \"\"\"Checks and corrects grammar mistakes.\"\"\"\n",
    "    log_command(update, context)\n",
    "    user_input = ' '.join(context.args).strip().lower()\n",
    "    \n",
    "    if not user_input:\n",
    "        await update.message.reply_text(\"❗ Please provide a sentence after /correct.\")\n",
    "        return\n",
    "    \n",
    "    matches = tool.check(user_input)\n",
    "    \n",
    "    if not matches:\n",
    "        response = \"✅ No grammar mistakes detected.\"\n",
    "    else:\n",
    "        corrected_text = language_tool_python.utils.correct(user_input, matches)\n",
    "        response = f\"✏️ **Correction:** {corrected_text}\"\n",
    "    \n",
    "    await update.message.reply_text(response)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "18084174-82d7-460f-9eed-719344b82273",
   "metadata": {},
   "outputs": [],
   "source": [
    "async def vocabinfo_command (update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:\n",
    "    \"\"\"Provides definition and synonyms of a word.\"\"\"\n",
    "    log_command(update, context)\n",
    "    user_input = ' '.join(context.args).strip().lower()\n",
    "    \n",
    "    if not user_input:\n",
    "        await update.message.reply_text(\"🔍 Please provide a word after /vocabinfo.\")\n",
    "        return\n",
    "    \n",
    "    synsets = wordnet.synsets(user_input)\n",
    "    \n",
    "    if not synsets:\n",
    "        await update.message.reply_text(f\"❌ Sorry, no definition found for '{user_input}'.\")\n",
    "    else:\n",
    "        definition = synsets[0].definition()\n",
    "        synonyms = [lemma.name() for lemma in synsets[0].lemmas()]\n",
    "        \n",
    "        message = f\"📖 **Word:** {user_input.capitalize()}\\n\"\n",
    "        message += f\"💡 **Definition:** {definition}\\n\"\n",
    "        if synonyms:\n",
    "            message += f\"📝 **Synonyms:** {', '.join(synonyms)}\"\n",
    "        \n",
    "        await update.message.reply_text(message, parse_mode='Markdown')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "dca33256-7636-4325-b4d2-b5a1556334f1",
   "metadata": {},
   "outputs": [],
   "source": [
    "async def reset_command(update: Update, context: ContextTypes):\n",
    "    log_command( update, context)\n",
    "    context.user_data.clear()  # Clears stored user data\n",
    "    await update.message.reply_text(\"🔄 Session has been reset. You can start fresh now!\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "7b833e20-2b44-4a68-b1f6-f6768f4c42ce",
   "metadata": {},
   "outputs": [],
   "source": [
    "async def handle_message(update: Update, context: CallbackContext) -> None:\n",
    "    user_text = update.message.text\n",
    "\n",
    "    # Check if the message starts with a command\n",
    "    if user_text.startswith('/correct'):\n",
    "        await update.message.reply_text(\"❗ Please provide a sentence after /correct. Example: /correct She go to school.\")\n",
    "        return\n",
    "    elif user_text.startswith('/vocabinfo'):\n",
    "        await update.message.reply_text(\"❗ Please provide a word after /vocabinfo. Example: /vocabinfo happy.\")\n",
    "        return\n",
    "\n",
    "    # Check for grammar issues in the message using LanguageTool\n",
    "    matches = tool.check(user_text)\n",
    "    corrected_text = language_tool_python.utils.correct(user_text, matches)\n",
    "\n",
    "    if user_text.lower() == corrected_text.lower():\n",
    "        response = \"Your sentence looks good! ✅\"\n",
    "    else:\n",
    "        response = f\"Here's a suggestion:\\n{corrected_text}\"\n",
    "\n",
    "    # Log the original and corrected text\n",
    "    logger.info(f\"User input: {user_text} | Corrected: {corrected_text}\")\n",
    "    \n",
    "    # Send the response back to the user\n",
    "    await update.message.reply_text(response)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "29f82528-d151-41ce-a574-075dbbc40872",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# Set bot's timezone\n",
    "timezone = pytz.timezone('Asia/Riyadh')\n",
    "dt = datetime.now(timezone)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "7b045870-983a-4196-b378-4994402b4ca5",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Running bot...\n"
     ]
    }
   ],
   "source": [
    "async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):\n",
    "    logging.error(f\"Update {update} caused error {context.error}\")\n",
    "if __name__=='__main__':\n",
    "    logging.info('Starting bot...')\n",
    "# Initialize bot application\n",
    "    app= Application.builder().token(TELEGRAM_TOKEN).build()\n",
    "    #add command handler\n",
    "    app.add_handler(CommandHandler('start', start_command))\n",
    "    app.add_handler(CommandHandler('help', help_command))\n",
    "    app.add_handler(CommandHandler('correct', correct_command))\n",
    "    app.add_handler(CommandHandler('vocabinfo', vocabinfo_command))\n",
    "    app.add_handler(CommandHandler('reset', reset_command))\n",
    "\n",
    "    #add message handler\n",
    "    app.add_handler(MessageHandler(filters.TEXT, handle_message)) \n",
    " \n",
    "    #add error handler\n",
    "    app.add_error_handler(error)\n",
    "    \n",
    "    nest_asyncio.apply()\n",
    "\n",
    "\n",
    "async def run_bot():\n",
    "    logging.info('Polling...')\n",
    "    await app.run_polling(poll_interval=3)\n",
    "\n",
    "# Start the bot\n",
    "asyncio.create_task(run_bot())\n",
    "print(\"Running bot...\")\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b3e5391e-55fb-44c1-b9a2-5bcf803865c9",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
