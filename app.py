from flask import Flask, render_template, redirect, request
import requests
import psycopg2
import json
import os
import database_functions

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
app.config['SECRET_KEY'] = 'hello'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/movies')
def movies():
    results = database_functions.sql_fetch('SELECT id, title, release_year, img_src FROM movies',[])
    # conn = psycopg2.connect(DB_URL)
    # cur = conn.cursor()
    # cur.execute('SELECT title, release_year, img_src FROM movies;')
    # results = cur.fetchall()
    # print(results)
    # conn.close()
    return render_template('movies.html', results = results)

@app.route('/movie')
def movie():
    id = request.args.get('id')
    results = database_functions.sql_fetch('SELECT imdb_id, title, release_year, img_src, whose_pick, country, synopsis, date_watched FROM movies WHERE id = %s',[id])
    return render_template('movie.html', results = results)

#initially just to display a search result from imdb
@app.route('/poll_creator')
def poll_creator():
    search_term = "North by Northwest"
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
    search_term = request.args.get('movie_search')
    movie_id_to_add = request.args.get('id')
    if search_term:
        response = requests.get(f'https://imdb-api.com/en/API/SearchTitle/' + API_KEY + '/' + search_term + '/')
        response_json = response.json()
        results = response_json['results']
        print(results)
        return render_template('add_movie.html', results = results)
    else:
        if movie_id_to_add:
            conn = psycopg2.connect(DB_URL)
            cur = conn.cursor()
            cur.execute('SELECT title, release_year, whose_pick, img_src FROM movies WHERE imdb_id = %s', [movie_id_to_add])
            database_results = cur.fetchall()
            # conn.close()
            if database_results:
                # say "it's already in there"
                film_exists = 'this movie is already in the database, WE ALREADY WATCHED IT'

                return render_template('add_movie.html', oliver = film_exists, database_results = database_results)
            else:
                response = requests.get(f'https://imdb-api.com/en/API/Title/' + API_KEY + '/' + movie_id_to_add + '/')
                response_json = response.json()
                print('JIMIN')
                print(response_json)
                movie_to_add_api_results = response_json
                film_doesnt_exist = 'this movie is not in the database - we can try to add it now'
                return render_template('add_movie.html', film_doesnt_exist = film_doesnt_exist, movie_to_add_api_results = movie_to_add_api_results)    
        else:
            return render_template('add_movie.html')

@app.route('/add_movie_action', methods=['POST'])
def add_movie_action():
        imdb_id = request.form.get('imdb_id')
        print('RM')
        print(imdb_id)
        whose_pick = request.form.get('whose_pick')
        print('JIN')
        print(whose_pick)
        title = request.form.get('title')
        print('JHOPE')
        print(title)
        date_watched = request.form.get('date_watched')
        print('JUNGKOOK')
        print(date_watched)
        country = request.form.get('country')
        print('V')
        print(country)
        release_year = request.form.get('release_year')
        print('suga')
        print(release_year)
        img_src = request.form.get('img_src')
        print('YOONGI')
        print(img_src)
        synopsis = request.form.get('synopsis')
        print('JK')
        print(synopsis)
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute('INSERT INTO movies (imdb_id, whose_pick, title, date_watched, country, release_year, img_src, synopsis) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', [imdb_id, whose_pick, title, date_watched, country, release_year, img_src, synopsis])
        conn.commit()
        conn.close()
        return redirect('/movies')
       

if __name__ == '__main__':
    app.run(debug=True)