#Neighborhood Blog Catalog

##About:
A simple [Flask](http://flask.pocoo.org/docs/0.10/) application which serves a user-contributable directory of neighborhood blogs. It is a submission for Project 3 in [Udacity’s Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004). This project, although functional, was built mostly for self-learning purposes.

##Instructions:
To build application:

1. Run `database_setup.py` to create the sqlalchemy database.
2. Run `lotsofblogs.py` to populate the database with the initial list of blogs.
3. Run `application.py` to run the Flask application on `localhost:5000`.

##Dependencies:
* [SQLAlchemy](http://www.sqlalchemy.org/)
* [Flask](http://flask.pocoo.org/)
* [httplib2](https://github.com/jcgregorio/httplib2)
* [Requests](http://www.python-requests.org/en/latest/)
* [Oauth2client](https://github.com/google/oauth2client)

##Citations:
* Course materials for Udacity's [Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088) and [Authentication & Authorization: OAuth](https://www.udacity.com/course/authentication-authorization-oauth--ud330) used in development of the project, with authentication & authorization methods implemented directly from course materials.
