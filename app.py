import pandas as pd

df_original = pd.read_excel("imdb_movie_summary.xlsx")
df = df_original.copy()

import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

stop_words = set(stopwords.words('english'))

from nltk import word_tokenize 
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def clean_text(text):
  tokens = word_tokenize(text)
  tokens_transformed = [lemmatizer.lemmatize(t.lower()) for t in tokens if t not in stop_words]
  s = ""
  for t in tokens_transformed:
    s = s + t + " "
  return s

df["transformed_summary"] = df["summary"].apply(clean_text)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer()


from sklearn.decomposition import NMF
model = NMF(n_components = 100)

from sklearn.preprocessing import Normalizer
scaler = Normalizer()

from sklearn.pipeline import make_pipeline
pipeline = make_pipeline(tfidf, model, scaler)

df_transformed = pd.DataFrame(pipeline.fit_transform(df.transformed_summary), index = df.titles)


import numpy as np
import model
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend',methods=['POST'])
def recommend():
    
    '''
    suggest movies based on input
    '''
    user_input = [x for x in request.form.values()]
    movie = user_input[0]
    key = df_transformed.loc[movie]
    scores = df_transformed.dot(key)
    recommendation_list = list(scores.nlargest(11).index)
        
    return render_template('recommend.html', recommendation_text=recommendation_list[1:])

if __name__ == "__main__":
    app.run(debug=True)