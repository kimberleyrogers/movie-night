from flask import Flask, render_template, redirect
import requests
import psycopg2
import json
import os

DB_URL = os.environ.get("DATABASE_URL", "dbname=movie_night")

# for heroku database when ready
# DATABASE_URL = os.environ.get('DATBASE_URL', 'dbname=')
# SECRET_KEY = os.environ.get('SECRET_KEY', '4b8c7ba7452ebd7c48195ee1d36b5604')

# for imdb API
API_KEY = 'k_f11wle6a'

# imdb API search URLs
SEARCH_TITLE_URL = ('https://imdb-api.com/en/API/SearchTitle/k_f11wle6a/')
app = Flask(__name__)
# for heroku database ?
# app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movies')
def movies():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT title, release_year, img_src FROM movies;')
    results = cur.fetchall()
    print(results)
    conn.close()
    return render_template('movies.html', results = results)

#initially just to display a search result from imdb
@app.route('/poll_creator')
def poll_creator():
    search_term = "North by Northwest"
    # movie_params = {
    #     's': search_term,
    #     'apikey': API_KEY,
    # }

    # response = requests.get(f'http://www.omdbapi.com/', params = movie_params)
    response = requests.get(f'https://imdb-api.com/en/API/SearchTitle/' + API_KEY + '/' + search_term + '/')
    response_json = response.json()
    results = response_json['results']
    # response = requests.get(SEARCH_TITLE_URL.format(id=recipe_id), params=params)
    # RESPONSE_json = response.json()
    # title = RESPONSE_json['title']

    print(results)
    return render_template('poll_creator.html', results = results)

@app.route('/add_movie')
def add_movie():
    search_term = "North by Northwest"
    # movie_params = {
    #     's': search_term,
    #     'apikey': API_KEY,
    # }

    # response = requests.get(f'http://www.omdbapi.com/', params = movie_params)
    response = requests.get(f'https://imdb-api.com/en/API/SearchTitle/' + API_KEY + '/' + search_term + '/')
    response_json = response.json()
    results = response_json['results']
    # response = requests.get(SEARCH_TITLE_URL.format(id=recipe_id), params=params)
    # RESPONSE_json = response.json()
    # title = RESPONSE_json['title']

    print(results)
    return render_template('poll_creator.html', results = results)

if __name__ == '__main__':
    app.run(debug=True)