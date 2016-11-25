#Neighborhood Blog Catalog

##About:
A simple [Flask](http://flask.pocoo.org/docs/0.10/) application which serves a user-contributable directory of neighborhood blogs. It is a submission for Project 3 in [Udacity’s Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004). This project, although functional, was built mostly for self-learning purposes. I am currently working on getting it up and running on Heroku [here](neighborhood-blogs-app.herokuapp.com).

##Instructions:
To build application:

1. Run `database_setup.py` to create the sqlalchemy database.
2. Run `lotsofblogs.py` to populate the database with the initial list of blogs.
3. Run `application.py` to run the Flask application on `localhost:5000`.

Note: In order for authentication and authorization methods to work properly, a [Google](console.developers.google.com) client ID and client secret must be provided. I have not included mine in the public repository; to run the application you may provide your own in the `client_secrets.json` placeholder text.

##Dependencies:
* [SQLAlchemy](http://www.sqlalchemy.org/)
* [Flask](http://flask.pocoo.org/)
* [httplib2](https://github.com/jcgregorio/httplib2)
* [Requests](http://www.python-requests.org/en/latest/)
* [Oauth2client](https://github.com/google/oauth2client)

##References:
* Course materials for Udacity's [Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088) and [Authentication & Authorization: OAuth](https://www.udacity.com/course/authentication-authorization-oauth--ud330).
