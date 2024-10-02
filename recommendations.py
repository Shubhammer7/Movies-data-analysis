import ast
import string
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

# Load the dataset
def load_data():
    df = pd.read_csv("tmdb_5000_movies.csv")
    return df


# Clean the data
def clean_keywords(keywords_str):
    try:
        keywords_list = ast.literal_eval(keywords_str)
        keywords = [keyword['name'] for keyword in keywords_list]
        return keywords
    except (ValueError, SyntaxError):
        return []


def clean_genres(genre_str):
    try:
        genre_list = ast.literal_eval(genre_str)
        genres = [genre['name'] for genre in genre_list]
        return genres
    except (ValueError, SyntaxError):
        return []


def clean_data(df):
    df_new = df.drop(['homepage', 'tagline'], axis=1)
    df_recommendation = df_new[['title', 'genres', 'keywords', 'overview']]

    df_recommendation['overview'] = df_recommendation['overview'].fillna('').str.lower()
    df_recommendation['overview'] = df_recommendation['overview'].apply(
        lambda x: x.translate(str.maketrans('', '', string.punctuation))
    )

    df_recommendation['genres'] = df_recommendation['genres'].apply(clean_genres)
    df_recommendation['keywords'] = df_recommendation['keywords'].apply(clean_keywords)

    df_recommendation['combined_features'] = (
            df_recommendation['genres'].astype(str) + ' ' +
            df_recommendation['keywords'].astype(str) + ' ' +
            df_recommendation['overview'].astype(str)
    )

    df_recommendation['combined_features'] = df_recommendation['combined_features'].str.replace("[", "").replace("]",
                                                                                                                 "").replace(
        "'", "").strip()

    return df_recommendation


# Generate TF-IDF matrix and cosine similarity
def generate_similarity(df_recommendation):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df_recommendation['combined_features'])
    cosine_sim = cosine_similarity(tfidf_matrix)
    return cosine_sim


# Get movie recommendations
def get_recommendations(title, df_recommendation, cosine_sim):
    # Get the index of the movie that matches the title
    try:
        idx = df_recommendation[df_recommendation['title'] == title].index[0]

        # Get the pairwise similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        return df_recommendation.iloc[movie_indices]
    except IndexError:
        return pd.DataFrame()  # Return an empty DataFrame if no movie found



# Main function to run the recommendations
if __name__ == "__main__":
    df = load_data()
    df_recommendation = clean_data(df)
    cosine_sim = generate_similarity(df_recommendation)

    # Example usage
    recommended_movies = get_recommendations('The Shawshank Redemption', df_recommendation, cosine_sim)
    if recommended_movies is not None:
        print(recommended_movies[['title', 'genres', 'combined_features']])
    else:
        print("Movie not found.")
