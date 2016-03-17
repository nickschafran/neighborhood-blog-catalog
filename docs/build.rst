Building from source:
=====================

1. Run ``database_setup.py`` to create the sqlalchemy database.
2. Run ``lotsofblogs.py`` to populate the db with the initial list of blogs.
3. Run ``application.py`` to run the Flask application on `localhost:5000`.

Note: In order for authentication and authorization methods to work properly,
a `Google <console.developers.google.com>`_ client ID and client secret must
be provided. I have not included mine in the public repository; to run the
application you may provide your own in the `client_secrets.json` placeholder
text.