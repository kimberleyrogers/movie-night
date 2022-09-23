![title](./static/images/title.jpeg)

## 🎬 ABOUT
This project was built to celebrate an ongoing weekly tradition with a group of friends.
Each Monday we take turns to create a movie poll whilst the rest of us vote on which movie we'd like to watch. We've watched dozens of movies through Monday movie night.

I wanted to create a visual of all the films we've watched, who picked them and show some movie data; like country of origin, genre, runtime etc.

## 👉🏽 VISIT
[Click here to visit my Movie Night website](https://thawing-woodland-36245.herokuapp.com/)

## 📚 HOW TO USE 

The site consists of:
+ the movie list - every film watched at movie night, linking to a page per movie with more information
+ members page - a picture for each member, linking to a page per member with a list of their movie choices
+ search feature - accessing the [imdb api](https://imdb-api.com/), search by title, actor, genre, award category
+ after finding a title using search, add it to the movie list or to your poll
+ make a poll feature - save movies you like to your poll


## 🖥 TECHNICAL
Deployed full stack CRUD website built with Python, Flask, Jinja, HTML, CSS, postgreSQL and utilising a RESTful movie website API.

To run yourself:
+ Import the requirements.txt file
+ Install and activate python virtual environment
+ Create an account at https://imdb-api.com/ and generate a key to utilise the API
+ Store the API key locally in a variable named MY_API_KEY
+ Create a local database in psql named 'movie_night'
+ Load the schema.sql file to create tables
+ Load the seed_users.sql file first to add users - or create your own for a customised experience
+ Load the seed_movies.sql file to add a few movies - use the 'add movie' feature to customise 


## 🤖 FUTURE
Whilst this is a personal project for use with my friends, I'd like to create a version which allows a user and a nominated group of their friends, family, coworkers to use the framework to create their own movie night and store their picks.

+ Add a password protection to the 'add movie' function for data integrity
+ Expand the genre search to include more genres
+ Export a list of the current movie data to create a seed_movies.sql file for safekeeping
+ Enable sharing of 'your poll' feature
+ Analyse the movie data to generate factoids for each member page, and generally for the movie data


## 🪳 BUGS

+ Database and table properties have limitations on string length, so longer synopses or film titles from imdb API can crash the page when trying to store in the database
+ I misunderstood the actor search function on the API - it returns individual actors as opposed to the movies they have starred in. Doesn't make a lot of sense to add "Anne Hathaway" to your movie poll!
+ Advanced Search is limited to a few genres as I ran out of time - so I hope you're looking for Action, Biography or Crime!
+ My site is open for everyone, so anyone can add or delete - good for demo purposes, bad for data integrity.

