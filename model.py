import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize 
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline


nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
stop_words = set(stopwords.words('english'))





def clean_text(text):
  tokens = word_tokenize(text)
  tokens_transformed = [lemmatizer.lemmatize(t.lower()) for t in tokens if t not in stop_words]
  s = ""
  for t in tokens_transformed:
    s = s + t + " "
  return s


def make_df():
    df_original = pd.read_excel("imdb_movie_summary.xlsx")
    df = df_original.copy()
    df["transformed_summary"] = df["summary"].apply(clean_text)    
    
    tfidf = TfidfVectorizer() 
    
    
    model = NMF(n_components = 100)
    
    
    scaler = Normalizer()
    
    
    pipeline = make_pipeline(tfidf, model, scaler)
    
    df_transformed = pd.DataFrame(pipeline.fit_transform(df.transformed_summary), index = df.titles)
    return df_transformed

df = make_df()
df.to_excel("df_transformed.xlsx")