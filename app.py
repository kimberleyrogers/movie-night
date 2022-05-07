from flask import Flask, render_template, redirect, request
import requests
import psycopg2
import json
import os
import functions

DB_URL = os.environ.get("DATABASE_URL", "dbname=movie_night")
API_KEY = os.environ.get("MY_API_KEY")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/movies')
def movies():
    # requests all records from movies table
    results = functions.sql_fetch('SELECT id, title, release_year, img_src FROM movies',[])
    return render_template('movies.html', results = results)

@app.route('/movie')
def movie():
    # requests id of movie that was clicked, find it's information from movie table and linked user name from user table
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
    # checks for values from the 4 search functions
    title_search = request.args.get('movie_search')
    actor_search = request.args.get('actor_search')
    advanced_search_genre = request.args.get('genre')
    advanced_search_awards = request.args.get('awards')
    if title_search:
        # if searched by title, request results from imdb
        response = requests.get(f'https://imdb-api.com/en/API/SearchTitle/' + API_KEY + '/' + title_search + '/')
        response_json = response.json()
        results = response_json['results']
        if results:
            # if imdb returns any results
            return render_template('add_movie.html', results = results)
        else:
            # if imdb returns nothing or call fails
            no_results = "Sorry, we didn't find anything matching " + title_search
            return render_template('add_movie.html', no_results = no_results)
    elif actor_search:
        # if searched by actor, request results from imdb
        response = requests.get(f'https://imdb-api.com/en/API/SearchName/' + API_KEY + '/' + actor_search + '/')
        response_json = response.json()
        results = response_json['results']
        if results:
            # if imdb returns any results
            return render_template('add_movie.html', results = results)
        else:
            # if imdb returns nothing or call fails
            no_results = "Sorry, we didn't find anything matching " + actor_search
            return render_template('add_movie.html', no_results = no_results)
    elif advanced_search_genre or advanced_search_awards:
         # if searched by actor, request results from imdb
        movie_params = {
            'genres': advanced_search_genre,
            'groups': advanced_search_awards,
            'apikey': API_KEY
        }
        response = requests.get(f'https://imdb-api.com/API/AdvancedSearch/', movie_params)   
        response_json = response.json()
        results = response_json['results']
        if results:   
            # if imdb returns any results 
            return render_template('add_movie.html', results = results)   
        else:
            # if imdb returns nothing or call fails
            no_results = "Sorry, we didn't find anything matching " + advanced_search_awards + " and " + advanced_search_genre
            return render_template('add_movie.html', no_results = no_results)
    else:
        #before search is run, just renders page with search function
        return render_template('add_movie.html')

@app.route('/add_movie_confirm', methods=['GET'])
def add_movie_confirm():
    # gets id of movie selected and checks if it exists in movies table and pull key info
    movie_id_to_add = request.args.get('id')
    database_results = functions.sql_fetch('SELECT title, release_year, whose_pick, img_src FROM movies WHERE imdb_id = %s', [movie_id_to_add])
    if database_results:
        # if movie in movies table, find related name for user id in users table
        member_name = database_results[0][2]
        member_first_name = functions.sql_fetch('SELECT name FROM users WHERE id = %s', [member_name])
        member_first_name_tidy = member_first_name[0][0]
        film_exists = 'We already have a record of watching this film!'
        return render_template('add_movie_confirm.html', film_exists = film_exists, database_results = database_results, member_first_name_tidy = member_first_name_tidy)
    else:
        # if movie not in movies table, use id to get key info from imdb
        # render page to ask user for additional info (who's pick and date watched)
        response = requests.get(f'https://imdb-api.com/en/API/Title/' + API_KEY + '/' + movie_id_to_add + '/')
        response_json = response.json()
        movie_to_add_api_results = response_json
        film_doesnt_exist = 'this movie is not in the database - we can try to add it now'
        return render_template('add_movie_confirm.html', film_doesnt_exist = film_doesnt_exist, movie_to_add_api_results = movie_to_add_api_results)

@app.route('/add_movie_action', methods=['POST'])
def add_movie_action():
    # grab key info from prior page and insert into movies table to store new film.
    info = functions.grab_info_movies_watched()
    functions.sql_write('INSERT INTO movies (imdb_id, whose_pick, title, date_watched, country, release_year, img_src, synopsis) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', info)
    return redirect('/movies')

@app.route('/add_poll_action', methods=['POST'])
def add_poll_action():
    # using movie id, gets key info from imdb and enters into poll table
    # would love to change this name below from kimbo to something relevant, but everytime I do, it breaks and I don't know why :(
    search_term = request.form.get('kimbo')
    print('jimin')
    print(search_term)
    response = requests.get(f'https://imdb-api.com/en/API/Title/' + API_KEY + '/' + search_term + '/')
    response_json = response.json()
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
    # checks if anything in poll table
    poll_content = functions.sql_fetch('SELECT imdb_id, title, img_src, runtime_mins, genre, release_year from poll;')
    if poll_content:
        # renders page with all movies from poll table
        return render_template('your_poll.html', poll_content = poll_content)
    else:
        # renders page with error message
        poll_empty_message = "Your poll is empty. Search for a movie to add to your next movie night poll."
        return render_template('your_poll.html', poll_empty_message = poll_empty_message)

@app.route('/clear_poll_action')
def clear_poll_action():
    # clears all results from poll table
    functions.sql_write('TRUNCATE TABLE poll;')
    return redirect('/your_poll')

@app.route('/members')
def members():
    # requests user info from user table and displays on page
    results = functions.sql_fetch('SELECT id, name FROM users', [])
    return render_template('members.html', results = results)

@app.route('/member', methods=['GET'])
def member():
    # takes user id from link and retrieves their info from users tables, and their movies from movies table
    user_id = request.args.get('id')
    results = functions.sql_fetch('SELECT name FROM users WHERE id = %s', [user_id])
    name = results[0][0]
    results = functions.sql_fetch('SELECT id, title, release_year, img_src FROM movies WHERE whose_pick = %s', [user_id])
    return render_template('member.html', name = name, user_id = user_id, results = results)

if __name__ == '__main__':
    app.run(debug=True)