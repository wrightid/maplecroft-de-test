
Define marshmallow schema for site and return all sites

Add requests to requirements for remote API access

migrations/versions, models/site.py - define site table, uses string for coordinates due to SQLlite limitations

Add clean target to Makefile to make it easier to start again

Add migrations directory to the docker-compose.yml file to make it easier to access db change scripts (Aware that there are still permission issues since the container is running as root)
 
Modify Makefile to allow creation of migration scripts
    - ```make db-revision ARGS='-m "create sites table"'```
    - Equivalent to ```docker-compose exec web flask db revision -m 'Create sites table'```



