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
    
    
    pipeline = make_pipeline(tfidf, model)
    
    df_transformed = pd.DataFrame(pipeline.fit_transform(df.transformed_summary), index = df.titles)
    
    genre_master = ["drama", "comedy", "romance", "horror", "action", "sci-fi", "sport", "fantasy", "crime", "music", "war", "biography", "thriller", "mystery", "family", "animation", "adventure", "musical", "history", "western", "film-noir" ]
    genre_dict = {"drama": 1, "comedy": 2, "romance": 3, "horror": 4, "action": 5, "sci-fi": 6, "sport":7, "fantasy": 8, "crime":  9, "music": 10, "war": 11, "biography": 12, "thriller": 13, "mystery": 14, "family": 15, "animation": 16, "adventure": 17, "musical": 18, "history": 19, "western": 20, "film-noir": 21}
    full = []
    for g in df.genre:
      g = g.lower()
      ind = [genre_dict.get(x) for x in g.split(", ")]
      temp = []
      for i in range(1, len(genre_master) + 1):
        if i in ind:
          temp.append(1)
        else:
          temp.append(0)
      full.append(temp)
      
      df_genre = pd.DataFrame(full, columns = genre_master, index = df.titles)
      df_combined = pd.DataFrame(scaler.fit_transform(pd.concat([df_transformed, df_genre], axis = 1)), index = df.titles)
    
    
    return df_combined
df = make_df()
df.to_excel("df_transformed.xlsx")
