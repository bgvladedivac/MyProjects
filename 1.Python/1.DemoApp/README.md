A simple Flask application that let's you register and add your Favourite football teams.

The teams are persistent into the db layer.

Developed for the purpose of being referenced inside custom AWS AMIs, Docker image and pipeline scenarios.

It's just an extended version of hello_world, but provides a db as well :)

Database support any SQL_Alchemy engine. The endpoint must be expressed as an environment varibale called 'FOOTBALL_APP_DB'. In case it's not found, the db lays on a local node endpoint 'sqlite:///database.db'
