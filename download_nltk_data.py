# -*- coding: utf-8 -*-

import nltk
# Specify the path to your local nltk_data folder
nltk.data.path.append('./nltk_data')

# Check if the required data is available
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
    print("All NLTK resources are available locally!")
except LookupError:
    print("One or more NLTK resources are missing.")
nltk.download('punkt', download_dir='C:/Users/thura/QalamBot/nltk_data')
nltk.download('stopwords', download_dir='C:/Users/thura/QalamBot/nltk_data')
nltk.download('wordnet', download_dir='C:/Users/thura/QalamBot/nltk_data')

import nltk

# Download required NLTK resources
resources = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
for resource in resources:
    nltk.download(resource)

print("NLTK resources downloaded successfully.")
