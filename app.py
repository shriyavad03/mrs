import streamlit as st
import pickle
import pandas as pd  # Correcting the import statement
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4dab62cab010e59ae54cd3e32544a16c'.format(movie_id))
    data = response.json()
    print(data)  # Add this line to print the API response
    poster_path = data.get('poster_path')
    return 'https://image.tmdb.org/t/p/w500' + poster_path


def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id  # Use the movie_id from the DataFrame
        print(f"Movie ID: {movie_id}, Title: {movies_df.iloc[i[0]].title}")

        # Fetch poster
        poster_url = fetch_poster(movie_id)

        recommended_movies_posters.append(poster_url)
        recommended_movies.append(movies_df.iloc[i[0]].title)

    return recommended_movies, recommended_movies_posters


# Load the pickled data
movies_list = pickle.load(open('moviedict.pkl', 'rb'))

# Create a DataFrame using the loaded data
movies_df = pd.DataFrame(movies_list)

# Load the similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Select a movie', movies_df['title'].values)
if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)



    col1, col2, col3, col4, col5 = st.columns(5)

    for i in range(5):
        with locals()[f'col{i + 1}']:
            if i < len(recommendations):
                st.text(recommendations[i])
                st.image(posters[i])
