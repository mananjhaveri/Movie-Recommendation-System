!pip install requests_html

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import itertools
from requests_html import HTML


#list of genres which will be used to alter urls to find movies across all genres
#genre = ["drama", "comedy", "romance", "horror", "action", "sci-fi", "sport", "fantasy", "crime", "music", "war", "biography", "thriller", "mystrey", "family", "animation" ]

titles = []
summary = []
year = []
genre = []
for i in range(1):
  page = 1
  #print(page)
  while(page < 4002):
    date = 0
    count = 0
    x = str(page)
    #url = r"https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&genres=" + g + "&languages=en&sort=user_rating,desc&start=" + x +"&explore=genres&ref_=adv_nxt"
    url = r"https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&countries=us&sort=user_rating,desc&start=" + x+"&ref_=adv_nxt"
    r = requests.get(url) 
    html_text = r.text
    r_html = HTML(html = html_text)
    r_title = r_html.find("h3 a")
    r_summary = r_html.find("p")
    r_year_genre = r_html.find("span")
  
    page = page + 50
    try:
      titles = titles + [r_title[x].text for x in range(0,50)]

      summary = summary + [r_summary[x].text for x in range(1,201, 4)]  
     
    except: 
      break
    

    for i in range(len(r_year_genre)):

        temp= re.findall("\d+", r_year_genre[i].text)

        if (r_year_genre[i].text.split(", ")[0]).lower() in genre_master:
          genre.append(r_year_genre[i].text)          

        elif (len(temp) > 0 and len(temp[0]) == 4):
          year.append(temp[0])
          
   
    
    
    
df = pd.DataFrame({"titles": titles, "summary": summary, "genre": genre, "year": year})
df.drop_duplicates(inplace=True, ignore_index=True)
df.to_excel("imdb_movie_summary.xlsx")
