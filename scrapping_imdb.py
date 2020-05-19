!pip install requests_html

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import itertools
from requests_html import HTML


#list of genres which will be used to alter urls to find movies across all genres
genre = ["drama", "comedy", "romance", "horror", "action", "sci-fi", "sport", "fantasy", "crime", "music", "war", "biography", "thriller", "mystrey", "family", "animation" ]

titles = []
summary = []

for g in genre:
  i = 1
  while(True):
    x = str(i)
    url = r"https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&genres=" + g +"&languages=en&start=" + x + "&explore=genres&ref_=adv_nxt" 
    r = requests.get(url) 
    html_text = r.text
    r_html = HTML(html = html_text)
    r_title = r_html.find("h3 a")#for title
    r_summary = r_html.find("p")#for summary. Every 4th item is the summary, will iterated accordingly
  
    i = i + 50
    try:
      titles = titles + [r_title[x].text for x in range(0,50)]
      summary = summary + [r_summary[x].text for x in range(1,201, 4)]
      print(g," ", x)
    except: 
      break
    
    
df = pd.DataFrame({"titles": titles, "summary": summary})
df.drop_duplicates(inplace=True, ignore_index=True)
df.to_excel("imdb_movie_summary.xlsx")