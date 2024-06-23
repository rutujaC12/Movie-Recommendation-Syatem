import streamlit as st
import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from requests.exceptions import RequestException

# Load data
@st.cache_data
def load_data():
    credits_df = pd.read_csv("credits.csv")
    movies_df = pd.read_csv("movies.csv")
    movies_df = movies_df.merge(credits_df, on='title')
    return movies_df

movies_df = load_data()

# Data preprocessing
def preprocess_data(movies_df):
    movies_df = movies_df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'crew']]
    movies_df.dropna(inplace=True)

    def convert(obj):
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L

    movies_df['genres'] = movies_df['genres'].apply(convert)
    movies_df['keywords'] = movies_df['keywords'].apply(convert)

    def fetch_director(obj):
        L = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
        return L

    movies_df['crew'] = movies_df['crew'].apply(fetch_director)
    movies_df['overview'] = movies_df['overview'].apply(lambda x: x.split())
    movies_df['genres'] = movies_df['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies_df['keywords'] = movies_df['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies_df['crew'] = movies_df['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

    movies_df['tags'] = movies_df['overview'] + movies_df['genres'] + movies_df['keywords'] + movies_df['crew']
    new_df = movies_df[['movie_id', 'title', 'tags']]
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
    return new_df

new_df = preprocess_data(movies_df)

# Build recommendation model
def build_model(new_df):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    cosine_sim = cosine_similarity(vectors)
    return cosine_sim

cosine_sim = build_model(new_df)

# TMDb API configuration
API_KEY = 'e259b4560b93c106eb2e22eb5714d4a4'
BASE_URL = 'https://api.themoviedb.org/3'
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/w500'

def fetch_poster(movie_title):
    search_url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={movie_title}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            full_poster_url = f"{POSTER_BASE_URL}{poster_path}"
            return full_poster_url
    except RequestException as e:
        st.error(f"Error fetching poster for {movie_title}: {e}")
    return None

# Recommendation function
def recommend(movie):
    if movie not in new_df['title'].values:
        return []
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = cosine_sim[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [new_df.iloc[i[0]].title for i in movie_list]
    return recommended_movies

# Streamlit UI
st.title("Movie Recommendation System")

movie_list = new_df['title'].values
selected_movie = st.selectbox("Select a movie you like:", [""] + list(movie_list))

if st.button('Recommend'):
    recommendations = recommend(selected_movie)
    if recommendations:
        st.write(f"If you like **{selected_movie}**, you might also like:")
        for movie in recommendations:
            poster_url = fetch_poster(movie)
            if poster_url:
                st.image(poster_url, width=150)
                st.write(movie)
            else:
                st.write(f"{movie} (Poster not found)")
    else:
        st.write("No recommendations found. Please check the movie title.")
