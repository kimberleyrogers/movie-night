# movie night project

https://thawing-woodland-36245.herokuapp.com/

![title](/static/images/title.jpeg)

## overview
This project was built to celebrate an ongoing weekly tradition with a group of friends.
Each Monday we hold a movie night, and take turns to create a movie poll (with a loose theme) whilst the rest of us vote on which movie we'd like to watch from the poll. We've watched dozens of movies through Monday movie night.

I wanted to create a visual of all the films we've watched, who picked them and some movie data; like country of origin, genre, runtime etc.

The site consists of:
+ home page with logo
+ about page
+ the movie list - every film watched at movie night
+ individual movie pages with more information
+ members page - a picture for each member
+ individual member page - name, picture and a list of their movie choices
+ search feature - accessing the imdb api, search by title, actor, genre, award category
+ after finding a title using search, add it to the movie database or a poll creator
+ make a poll feature - save movies you like the look of to your poll


## languages
Built with Python, HTML, CSS, SQL.


## technical requirements
+ Import the requirements.txt file
+ Install and activate python virtual environment
+ Create an account at https://imdb-api.com/ and generate a key to utilise the API
+ Store the API key locally in a variable named MY_API_KEY
+ Create a local database in psql named 'movie_night'
+ Load the schema.sql file to create tables
+ Load the seed_users.sql file first to add users - or create your own for a customised experience
+ Load the seed_movies.sql file to add a few movies - use the 'add movie' feature to customise 


## future iterations
Whilst this is a personal project for use with the OG movie night crew, I'd like to create a version which allows a user and a nominated group of their friends, family, coworkers to use the framework to create their own movie night and store their picks.

+ update database and table properties to accept longer strings from imdb API
+ add a password protection to the 'add movie' function for data integrity
+ expand the genre search to include more genres
+ adjust the actor search to find films starring those actors instead of the actors themselves
+ export a list of the current movie data to create a seed_movies.sql file for safekeeping
+ enable sharing of 'your poll' feature
+ analyse the movie data to generate factoids for each member page, and generally for the movie data

## credit notes
This project was built for Unit 2 of General Assembly's Software Engineering Flex Immersive Course.  
The functions.py file was based on a template provided by Katie Bell.  
The CSS for the buttons is from https://getcssscan.com/css-buttons-examples  
The rest was crafted by me, Kimberley Rogers, with guidance and encouragement from my talented peers and instructors.