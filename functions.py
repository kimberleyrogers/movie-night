import os
import psycopg2
from flask import request

DB_URL = os.environ.get("DATABASE_URL", "dbname=movie_night")

# Run a SQL SELECT query and return all rows of results
# Example:
# results = sql_fetch('SELECT * FROM food WHERE id = %s', [id])
def sql_fetch(query, parameters=[]):
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute(query, parameters)
  results = cur.fetchall()
  conn.close()
  return results

# Run a SQL INSERT/UPDATE/DELETE query and do a commit.
# Example:
# sql_write('INSERT INTO food (name, price) VALUES (%s, %s)', [name, price])
def sql_write(query, parameters=[]):
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute(query, parameters)
  conn.commit()
  conn.close()

def grab_info_movies_watched():
  imdb_id = request.form.get('imdb_id')
  whose_pick = request.form.get('whose_pick')
  title = request.form.get('title')
  date_watched = request.form.get('date_watched')
  country = request.form.get('country')
  release_year = request.form.get('release_year')
  img_src = request.form.get('img_src')
  synopsis = request.form.get('synopsis')
  return [imdb_id, whose_pick, title, date_watched, country, release_year, img_src, synopsis]

def grab_info_poll():
  imdb_id = request.form.get('imdb_id')
  title = request.form.get('title')
  img_src = request.form.get('img_src')
  runtime_mins = request.form.get('runtime_mins')
  genre = request.form.get('genre')
  release_year = request.form.get('release_year')
  return [imdb_id, title, img_src, runtime_mins, genre, release_year]