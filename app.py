import streamlit as st
import pandas as pd
import numpy as np
import sklearn
import requests


def get_scores(title, cb_movies, cosine_sim):
    title_id = np.where(cb_movies['title']==title)[0][0]
    scores = []
    for key, value in enumerate(cosine_sim.iloc[title_id]):
        scores.append([key, value])
    return scores


def get_recommendations(cb_movies, scores):
    titles_id, budget, genres, homepage, overview = [], [], [], [], []
    production_companies, production_countries = [], []
    release_date, runtime, spoken_languages = [], [], []
    titles, vote_average, cast = [], [], []

    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    for i in scores[0:11]:
        titles.append(cb_movies.iloc[i[0]]['title'])
        titles_id.append(cb_movies.iloc[i[0]]['id'])
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

    return budget, genres, homepage, overview, production_companies, production_countries, release_date, runtime, spoken_languages, titles, vote_average, cast, titles_id


def get_image(title_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=393b66e59eb09a6adb154ec579586ae6&language=en-US'.format(title_id))
    data = response.json()
    error = {'success': False, 'status_code': 34, 'status_message': 'The resource you requested could not be found.'}
    url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/2048px-No_image_available.svg.png'
    if data != error:
        url = 'http://image.tmdb.org/t/p/w500' + data['poster_path']
    return url

def cb_columns(row_num, titles_id, movies):
    columns = st.columns(5)
    for i in range(5):
        with columns[i]:
            indx = i+1+(5*row_num)
            img = get_image(titles_id[indx])
            st.image(img)
            st.write(movies[indx])


def cb_style(budget, genres, homepage, overview, production_companies, production_countries, release_date, runtime, spoken_languages, titles, vote_average, cast, titles_id):
    st.title(titles[0])

    movie_img = get_image(titles_id[0])
    st.image(movie_img)

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
        cb_columns(i, titles_id, titles)


def get_similar_users():
    # Remove picked user ID from the candidate list
    user_similarity.drop(index=picked_userid, inplace=True)

    user_sim_thresh = 0.2

    # Get top 10 similar users
    similar_users = user_similarity[user_similarity[picked_userid]>user_sim_thresh][picked_userid].sort_values(ascending=False)[:10]

    return similar_users


def filter_movies(similar_users):
    # Movies that similar users watched. Remove movies that none of the similar users have watched
    similar_user_movies = movie_norm[movie_norm.index.isin(similar_users.index)].dropna(axis=1, how='all')

    # Movies that the target user has watched
    picked_userid_watched = movie_norm[movie_norm.index==0].dropna(axis=1, how='all')

    # Remove movies that target user watched
    similar_user_movies.drop(columns=picked_userid_watched.columns, errors='ignore', inplace=True)

    return similar_user_movies


def get_recom_movies(similar_user_movies, movies_df):
    # Get top 10 movies to recommend for target user
    scores = similar_user_movies.mean(axis=0).sort_values(ascending=False)[:10]
    rec_movies = scores.index.to_list()

    genres = movies_df[movies_df['title'].isin(rec_movies)]['genres'].to_list()

    return rec_movies, genres


def cf_style(rec_movies, genres):
    st.subheader('Recommendations:')

    num_rows = 2
    for i in range(num_rows):
        cf_columns(i, rec_movies, genres)


def cf_columns(row_num, rec_movies, genres):
    columns = st.columns(5)
    for i in range(5):
        with columns[i]:
            st.image(img)
            st.write('Title: ', rec_movies[i+(5*row_num)]) 
            st.write('Genres: ', genres[i+(5*row_num)])


# MAIN PAGE
st.header('Movie Recommendation System')

img = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/2048px-No_image_available.svg.png'

colab_sys = st.radio('Choose Recommendation System',
                     ['Content Based Recommendation System', 
                      'Colaborative Filtering Recommendation System'])


if colab_sys == 'Content Based Recommendation System':
    cb_movies = pd.read_csv('files/cb_movies.csv')
    cosine_sim = pd.read_csv('files/cosine_sim.csv')

    select_movie = st.selectbox('Type or choose movie', cb_movies['title'])
    button = st.button('Search')

    if button:
        scores = get_scores(select_movie, cb_movies, cosine_sim)
        budget, genres, homepage, overview, production_companies, production_countries, release_date, runtime, spoken_languages, titles, vote_average, cast, titles_id = get_recommendations(cb_movies, scores)
        cb_style(budget, genres, homepage, overview, production_companies, production_countries, release_date, runtime, spoken_languages, titles, vote_average, cast, titles_id)

else:
    user_similarity = pd.read_pickle('files/user_similarity.pkl')
    movie_norm = pd.read_csv('files/movie_pivot_normalized.csv')
    movies_df = pd.read_csv('files/movies.csv')

    picked_userid = st.slider('Pick user id', value=len(user_similarity.columns)-1)
    button = st.button(f'Show recommendations based on user {picked_userid} preferences')

    if button:
        sim_users = get_similar_users()
        sim_user_movies = filter_movies(sim_users)
        rec_movies, genres = get_recom_movies(sim_user_movies, movies_df)
        cf_style(rec_movies, genres)

