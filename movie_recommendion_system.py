# -*- coding: utf-8 -*-
"""
# **Movie Recommendation system**

By: Loai Nazeer
"""

# import modules
import pandas as pd
#import matplotlib as plt
import numpy as np
import nltk
#import gdown
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

nltk.download('punkt')
nltk.download('stopwords')



# Read the dataset
data = pd.read_csv("Data/TMDb_updated.CSV")
data.head(5)

data.isnull().values.any()

data.isnull().sum()

data=data.dropna()
data.isnull().sum()
data = data.reset_index(drop=True)

# tokenize the data
def tokenize(text):
    tokens = re.split("\W+", text)
    return tokens
data["overview"]= data["overview"].apply (lambda x: tokenize(x.lower()))

# remove stopwords
stop_words=set(stopwords.words("english"))
def remove_stopword(text):
    text_nostopword= [char for char in text if char not in stop_words]
    return text_nostopword

data["overview"]= data["overview"].apply(lambda x: remove_stopword(x))

# stemming 
ps = nltk.stem.porter.PorterStemmer()
def stem(data_no_stopword):
   text = [ps.stem ( word) for word in data_no_stopword]
   return text

data["overview"]= data["overview"].apply(lambda x: stem(x))

for i in range(0,len(data['overview'])):
  data["overview"][i] = str(data["overview"][i])

for i in range(0,len(data["overview"])):
  data["overview"][i] =  re.sub(r'\'|\[|\]|\,','',data["overview"][i])
data["overview"][2]

#Apply TF-IDF Trasformation
tfidf = TfidfVectorizer(stop_words='english')
data['overview'] = data['overview'] .fillna('')
tfidf_matrix = tfidf.fit_transform(data['overview'] )
tfidf_matrix.shape

################# Recommendation#############

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(data.index, index=data['title']).drop_duplicates()
data['title']=data['title'].drop_duplicates()
def get_recommendations(title,coun, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:coun]
    movie_indices = [i[0] for i in sim_scores]
    return data.iloc[movie_indices].sort_values(by=['vote_average'],ascending=False).reset_index(drop=True)

###### to search
def search_in_google(movie_title):
  query = "أكوام-مترجم"
  urls=[]
  for j in search(query+movie_title, tld="co.in", num=5, stop=5, pause=2):
      urls.append(j)
      #print(j)
  return urls

####################33
##urlss=[]
##for i in range(0,len(rec)):
##  urlss.append(search_in_google(rec['title'][i]))
##rec["url"]=urlss
##
