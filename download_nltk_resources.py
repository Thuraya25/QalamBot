import nltk
import os

# Set NLTK_DATA path
os.environ['NLTK_DATA'] = r"C:\Users\thura\QalamBot\nltk_data"
print(f"NLTK resources will be downloaded to: {os.environ['NLTK_DATA']}")

# Ensure the directory exists
if not os.path.exists(os.environ['NLTK_DATA']):
    os.makedirs(os.environ['NLTK_DATA'])

# Download the necessary NLTK resources
nltk.download('punkt', download_dir=os.environ['NLTK_DATA'])
nltk.download('stopwords', download_dir=os.environ['NLTK_DATA'])
nltk.download('words', download_dir=os.environ['NLTK_DATA'])
nltk.download('omw-1.4', download_dir=os.environ['NLTK_DATA'])
nltk.download('wordnet', download_dir=os.environ['NLTK_DATA'])

