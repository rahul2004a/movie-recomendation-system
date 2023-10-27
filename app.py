import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=b0c047df09c3e4c673c9e0090b314878&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def recommend(movie):
    
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')


movies_list = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl','rb'))


selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)


if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)

    if names:
        for i in range(len(names)):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(names[i])
            with col2:
                if posters[i]:
                    st.image(posters[i])
                else:
                    st.warning("Poster not available")
    else:
        st.warning("No recommendations available for the selected movie.")
