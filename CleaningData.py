# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 13:12:13 2016

@author: akhou
"""

import csv
import pandas as pd
import numpy as np
import re

WANTED_GENRE=[u'drama', u'action', u'adventure', u'animation',u'crime',u'fantasy',
u'music', u'mystery', u'romance', u'science fiction',
u'thriller', u'war', u'western',u'family film']

MOVIE_METADATA_FEATURES=["Wikipedia movie ID", "Freebase movie ID", "Movie name", "Movie release date", "Movie box office revenue", "Movie runtime", "Movie languages", "Movie countries", "Movie genres"]
PLOT_SUMMARY_FEATURES=["Wikipedia movie ID","Summary"]

DATA_SET_PRIMARY_FEATURES=["Movie genres","Summary"]
DATA_SET_FEATURES_TO_DROP=[x for x in MOVIE_METADATA_FEATURES if x not in DATA_SET_PRIMARY_FEATURES]

with open("MoviesSummaries/movie.metadata.tsv") as movie_metadata_file:
    movie_metadata_reader = csv.reader(movie_metadata_file, delimiter="\t") 
    movie_metadata_list=list(movie_metadata_reader)
    movie_metadata_data_set=df = pd.DataFrame.from_records(movie_metadata_list, 
        columns=MOVIE_METADATA_FEATURES)
with open("MoviesSummaries/plot_summaries.txt") as plot_summary_file: 
    plot_summary_reader = csv.reader(plot_summary_file, delimiter="\t") 
    plot_summary_list=list(plot_summary_reader)
    plot_summary_data_set=pd.DataFrame.from_records(plot_summary_list, 
        columns=PLOT_SUMMARY_FEATURES)
        
data_set=pd.merge(plot_summary_data_set,movie_metadata_data_set, on='Wikipedia movie ID')

data_set.drop(DATA_SET_FEATURES_TO_DROP,axis=1, inplace=True)
def replace_genre(genre_string):
    genre_list=genre_string.split(",")
    clean_genre_list=[]
    for genre in genre_list:
        genre_tuple=genre.split(':')
        if(len(genre_tuple)>1):
            clean_genre_list.append(genre_tuple[1])
    return clean_genre_list
     

for genre in WANTED_GENRE:
    data_set[genre]=data_set['Movie genres'].map(lambda x: 1 if x.lower().find(genre)!= -1 else 0)

data_set['Sum']=data_set.sum(axis=1, numeric_only=True)
data_set = data_set[data_set['Sum'] != 0]
data_set['Summary']=data_set['Summary'].map(lambda x: re.sub(' +',' ',x))
data_set['Summary'].replace('', np.nan, inplace=True)
data_set.dropna(subset=['Summary'], inplace=True)

#test=[]
#test=data_set.sum(numeric_only=True)

data_set.drop({'Movie genres','Sum'},axis=1, inplace=True)
data_set.to_csv("Movie_Summary.csv", sep=',', encoding='utf-8')      