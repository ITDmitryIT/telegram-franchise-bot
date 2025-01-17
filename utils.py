# utils.py
import re
import nltk
from nltk.corpus import stopwords
from natasha import MorphVocab

nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))
morph = MorphVocab()

def preprocess_text(text):
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', ' ', text)
    text = text.lower()
    tokens = text.split()
    tokens = [morph.parse(word)[0].normal_form for word in tokens if word not in stop_words]
    return ' '.join(tokens)