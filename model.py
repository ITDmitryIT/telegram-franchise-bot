# model.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd

def train_model(df):
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    X = tfidf_vectorizer.fit_transform(df['processed_question']).toarray()
    y = df['answer']
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return tfidf_vectorizer, model

def predict_answer(tfidf_vectorizer, model, question):
    vectorized_question = tfidf_vectorizer.transform([question]).toarray()
    return model.predict(vectorized_question)[0]