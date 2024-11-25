import pandas as pd
import numpy as np
import json

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

import matplotlib.pyplot as plt


df = pd.read_csv("tmdb_5000_movies.csv")

col_drop = ["homepage","genres","keywords","production_companies","production_countries","spoken_languages"]

df['keywords'] = df['keywords'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['genres'] = df['genres'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['production_companies'] = df['production_companies'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['production_countries'] = df['production_countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['spoken_languages'] = df['spoken_languages'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

def clean_cols(df):
    df['keywords_cl'] = df['keywords'].apply(
        lambda keywords: [item['name'] for item in keywords] if isinstance(keywords, list) else []
    )
    df['genres_cl'] = df['genres'].apply(
        lambda genres: [item['name'] for item in genres] if isinstance(genres, list) else []
    )
    df['production_companies_cl'] = df['production_companies'].apply(
        lambda production_companies: [item['name'] for item in production_companies] if isinstance(production_companies, list) else []
    )
    df['production_countries_cl'] = df['production_countries'].apply(
        lambda production_countries: [item['name'] for item in production_countries] if isinstance(production_countries, list) else []
    )
    df['spoken_languages_cl'] = df['spoken_languages'].apply(
        lambda spoken_languages: [item['name'] for item in spoken_languages] if isinstance(spoken_languages, list) else []
    )
    df['original_language'] = df['spoken_languages_cl'][0][0]

clean_cols(df)
df = df.drop(col_drop, axis=1)

text_data = df['genres_cl'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))

tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=1, stop_words='english')
tfidf_matrix = tf.fit_transform(text_data)

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

titles = df['title']
indices = pd.Series(df.index, index=df['title'])


def get_recommendations(title):
    idx = indices.get(title)  # Safely get the index for the movie
    if idx is None:
        return []  # If movie not found, return an empty list

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]

    # Extract only the 'title' column and convert to list
    return titles.iloc[movie_indices].tolist()
