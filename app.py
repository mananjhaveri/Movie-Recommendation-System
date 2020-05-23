import numpy as np
#import model
from flask import Flask, request, render_template
import pandas as pd
app = Flask(__name__)

def m(t):
    return t.lower()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend',methods=['POST'])
def recommend():
    
    '''
    suggest movies based on input
    '''
    user_input = [x for x in request.form.values()]
    movie = (user_input[0]).lower()
    df_transformed = pd.read_csv("df_combined.csv") #, index_col = "titles")
    df_transformed.titles = df_transformed.titles.apply(m)
    df_transformed.set_index("titles", inplace = True)
    
    
    try:
        
        key = df_transformed.loc[movie]
        if len(key) != 121:
            key = key.iloc[0]
        scores = df_transformed.dot(key)
        rec_list = list(scores.nlargest(11).index)
        recommendation_list = []
        for rec in rec_list:
            ww = ""
            for w in rec.split(" "):
                ww = ww + " " + w[0].upper() + w[1:]
            recommendation_list.append(ww)
    
    except:
        file1 = open("expansion_list.txt", "a")
        L = ["\n", movie]
        file1.writelines(L)
        file1.close() 
        recommendation_list = ["", "1. Check the spellings", "2. Enter title in original language", "If you still can't find the movie, it may not be currently available in our database. Try another movie"]
                               
    
    return render_template('recommend.html', recommendation_text=recommendation_list[1:])

if __name__ == "__main__":
    app.run(debug=True)
