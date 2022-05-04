from flask import Flask, render_template, redirect, request
import requests
import psycopg2
import json
import os
import functions

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
    results = functions.sql_fetch('SELECT id, title, release_year, img_src FROM movies',[])
    return render_template('movies.html', results = results)

@app.route('/movie')
def movie():
    id = request.args.get('id')
    results = functions.sql_fetch('SELECT movies.imdb_id, movies.title, movies.release_year, movies.img_src, movies.whose_pick, movies.country, movies.synopsis, movies.date_watched, users.name FROM movies, users WHERE movies.id = %s AND users.id = movies.whose_pick',[id])
    imdb_id = results[0][0]
    title = results[0][1]
    release_year = results[0][2]
    img_src = results[0][3]
    whose_pick = results[0][4]
    country = results[0][5]
    synopsis = results[0][6]
    date_watched = results[0][7]
    person = results[0][8]
    return render_template('movie.html', imdb_id = imdb_id, title = title, release_year = release_year, img_src = img_src, whose_pick = whose_pick, country = country, synopsis = synopsis, date_watched = date_watched, person = person)


@app.route('/add_movie')
def add_movie():
    search_term = request.args.get('movie_search')
    if search_term:
        response = requests.get(f'https://imdb-api.com/en/API/SearchTitle/' + API_KEY + '/' + search_term + '/')
        response_json = response.json()
        results = response_json['results']
        print(results)
        return render_template('add_movie.html', results = results)
    # else:
    #     if movie_id_to_add:
    #         conn = psycopg2.connect(DB_URL)
    #         cur = conn.cursor()
    #         cur.execute('SELECT title, release_year, whose_pick, img_src FROM movies WHERE imdb_id = %s', [movie_id_to_add])
    #         database_results = cur.fetchall()
    #         # conn.close()
    #         if database_results:
    #             # say "it's already in there"
    #             film_exists = 'this movie is already in the database, WE ALREADY WATCHED IT'
    #             return render_template('add_movie.html', film_exists = film_exists, database_results = database_results)
    #         else:
    #             response = requests.get(f'https://imdb-api.com/en/API/Title/' + API_KEY + '/' + movie_id_to_add + '/')
    #             response_json = response.json()
    #             print('JIMIN')
    #             print(response_json)
    #             movie_to_add_api_results = response_json
    #             film_doesnt_exist = 'this movie is not in the database - we can try to add it now'
    #             return render_template('add_movie.html', film_doesnt_exist = film_doesnt_exist, movie_to_add_api_results = movie_to_add_api_results)    
    else:
        return render_template('add_movie.html')

@app.route('/add_movie_confirm', methods=['GET'])
def add_movie_confirm():
    movie_id_to_add = request.args.get('id')
    database_results = functions.sql_fetch('SELECT title, release_year, whose_pick, img_src FROM movies WHERE imdb_id = %s', [movie_id_to_add])
    # conn = psycopg2.connect(DB_URL)
    # cur = conn.cursor()
    # cur.execute('SELECT title, release_year, whose_pick, img_src FROM movies WHERE imdb_id = %s', [movie_id_to_add])
    # database_results = cur.fetchall()
    # conn.close()
    if database_results:
        # say "it's already in there"
        film_exists = 'this movie is already in the database, WE ALREADY WATCHED IT'
        return render_template('add_movie_confirm.html', film_exists = film_exists, database_results = database_results)
    else:
        response = requests.get(f'https://imdb-api.com/en/API/Title/' + API_KEY + '/' + movie_id_to_add + '/')
        response_json = response.json()
        print('JIMIN')
        print(response_json)
        movie_to_add_api_results = response_json
        film_doesnt_exist = 'this movie is not in the database - we can try to add it now'
        return render_template('add_movie_confirm.html', film_doesnt_exist = film_doesnt_exist, movie_to_add_api_results = movie_to_add_api_results)

@app.route('/add_movie_action', methods=['POST'])
def add_movie_action():
    info = functions.grab_info_movies_watched()
    functions.sql_write('INSERT INTO movies (imdb_id, whose_pick, title, date_watched, country, release_year, img_src, synopsis) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', info)
    return redirect('/movies')

@app.route('/add_poll_action', methods=['POST'])
def add_poll_action():
    search_term = request.form.get('kimbo')
    print('rm')
    print(search_term)
    response = requests.get(f'https://imdb-api.com/en/API/Title/' + API_KEY + '/' + search_term + '/')
    response_json = response.json()
    print('jhope')
    print(response_json)
    imdb_id = response_json['id']
    title = response_json['title']
    img_src = response_json['image']
    runtime_mins = response_json['runtimeStr']
    genre = response_json['genres']
    release_year = response_json['year']
    functions.sql_write('INSERT INTO poll (imdb_id, title, img_src, runtime_mins, genre, release_year) VALUES (%s, %s, %s, %s, %s, %s);', [imdb_id, title, img_src, runtime_mins, genre, release_year])
    return redirect('/your_poll')

@app.route('/your_poll')
def your_poll():
    poll_content = functions.sql_fetch('SELECT imdb_id, title, img_src, runtime_mins, genre, release_year from poll;')
    # if poll_content:
    return render_template('your_poll.html', poll_content = poll_content)
    # else:
    #     return render_template('your_poll.html')

@app.route('/clear_poll_action')
def clear_poll_action():
    functions.sql_write('TRUNCATE TABLE poll;')
    return redirect('/your_poll')

if __name__ == '__main__':
    app.run(debug=True)


# movie_params = {
#     'title': title,
#     'apikey': 'k_f11wle6a',
#     'genres': genre,
#     'moviemeter': runtimemin, runtimemax,
#     'groups': top_250,oscar_nominees,razzie_nominees,
# }

#      response = requests.get(f'https://imdb-api.com/en/API/SearchTitle/' + API_KEY + '/' + search_term + '/')
#         'https://imdb-api.com/en/API/AdvancedSearch/' + API_KEY + '/' + search_term + '/')'