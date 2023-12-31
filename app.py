import streamlit as st
import pandas as pd
import numpy as np
import sklearn

def cf_suggestions(movie_name, movies_pivot):
        movie_index = np.where(movies_pivot.index == movie_name)[0][0]
        distances, suggestion = model.kneighbors(movies_pivot.iloc[movie_index, :].values.reshape(1,-1), n_neighbors=11)
        return suggestion[0]


def cf_recommendations(suggestions, movies_pivot, movies_df):
    movies = []
    genres = []

    for movieId in suggestions:
        movies.append(movies_pivot.index[movieId])

    for movie in movies:
        genre = movies_df[movies_df['title']==movie]['genres'].iloc[0]
        genres.append(genre)

    return movies, genres


def cf_style(movies, genres):
    st.title(movies[0])
    st.subheader('Genre: ' + ', '.join(genres[0]))
    st.image(img)
    
    st.subheader('Other recommendations:')

    num_rows = 2
    for i in range(num_rows):
        rec_columns(i, movies)


def rec_columns(row_num, movies):
    columns = st.columns(5)
    for i in range(5):
        with columns[i]:
            st.image(img)
            st.write(movies[i+1+(5*row_num)])


def get_scores(title, cb_movies, cosine_sim):
    title_id = np.where(cb_movies['title']==title)[0][0]
    scores = []
    for key, value in enumerate(cosine_sim.iloc[title_id]):
        scores.append([key, value])
    return scores


def get_recommendations(cb_movies, scores):
    budget, genres, homepage, overview = [], [], [], []
    production_companies, production_countries = [], []
    release_date, runtime, spoken_languages = [], [], []
    titles, vote_average, cast = [], [], []

    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    for i in scores[0:11]:
        titles.append(cb_movies.iloc[i[0]]['title'])
        genres.append(cb_movies.iloc[i[0]]['genres'])
        overview.append(cb_movies.iloc[i[0]]['overview'])
        budget.append(cb_movies.iloc[i[0]]['budget'])
        homepage.append(cb_movies.iloc[i[0]]['homepage'])
        production_companies.append(cb_movies.iloc[i[0]]['production_companies'])
        production_countries.append(cb_movies.iloc[i[0]]['production_countries'])
        release_date.append(cb_movies.iloc[i[0]]['release_date'])
        runtime.append(cb_movies.iloc[i[0]]['runtime'])
        spoken_languages.append(cb_movies.iloc[i[0]]['spoken_languages'])
        vote_average.append(cb_movies.iloc[i[0]]['vote_average'])
        cast.append(cb_movies.iloc[i[0]]['cast'])

    return budget, genres, homepage, overview, production_companies, production_countries, release_date, runtime, spoken_languages, titles, vote_average, cast


def cb_style(budget, genres, homepage, overview, production_companies, production_countries, release_date, runtime, spoken_languages, titles, vote_average, cast):
    st.title(titles[0])

    st.image(img)

    st.subheader('Overview')
    st.write(overview[0])

    st.subheader('Movie Info')
    st.write('Genre: ' + ', '.join(eval(genres[0])))
    st.write('Budget: ', str(budget[0]))
    st.write('Home page: ', homepage[0])
    st.write('Production companies: ' + ', '.join(eval(production_companies[0])))
    st.write('Production countries: ' + ', '.join(eval(production_countries[0])))
    st.write('Release date: ', release_date[0])
    st.write('Movie time: ' + runtime[0])
    st.write('Languages: ' + ', '.join(eval(spoken_languages[0])))
    st.write('Rating: ', str(vote_average[0]))
    st.subheader('Cast')
    st.write(', '.join(eval(cast[0])[0:10]) + ' and others')
    
    st.subheader('Other recommendations:')

    num_rows = 2
    for i in range(num_rows):
        rec_columns(i, titles)

# MAIN PAGE
st.header('Movie Recommendation System')

colab_sys = st.radio('Choose Recommendation System',
                     ['Content Based Recommendation System', 
                      'Colaborative Filtering Recommendation System'])


if colab_sys == 'Colaborative Filtering Recommendation System':

    model = pd.read_pickle('files/model.pkl')
    movies_df = pd.read_pickle('files/movies_df.pkl')
    movies_names = pd.read_pickle('files/movies_names.pkl')
    movies_pivot = pd.read_pickle('files/movies_pivot.pkl')

    img = 'https://www.vintagemovieposters.co.uk/wp-content/uploads/2023/03/IMG_1887-scaled.jpeg'

    select_movie = st.selectbox('Type or choose movie', movies_names)
    button = st.button('Search')

    if button:
        suggestion = cf_suggestions(select_movie, movies_pivot)
        movies, genres = cf_recommendations(suggestion, movies_pivot, movies_df)
        cf_style(movies, genres)

else:
    cb_movies = pd.read_csv('files/cb_movies.csv')
    cosine_sim = pd.read_csv('files/cosine_sim.csv')

    img = 'https://www.vintagemovieposters.co.uk/wp-content/uploads/2023/03/IMG_1887-scaled.jpeg'

    select_movie = st.selectbox('Type or choose movie', cb_movies['title'])
    button = st.button('Search')

    if button:
        scores = get_scores(select_movie, cb_movies, cosine_sim)
        budget, genres, homepage, overview, production_companies, production_countries, release_date, runtime, spoken_languages, titles, vote_average, cast = get_recommendations(cb_movies, scores)
        cb_style(budget, genres, homepage, overview, production_companies, production_countries, release_date, runtime, spoken_languages, titles, vote_average, cast)
    