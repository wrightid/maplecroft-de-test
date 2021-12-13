

Under normal circumstances I would look to use a GIS enabled database here e.g. postgres with postGIS but I felt that was out of scope for the task.

This would simplify the application and work better with larger datasets

Using a string to store the coordinates as decimal or point not supported in SQLlite and float won't store the data correctly

The area table isn't strictly necessary but it's helpful for doing a quick sanity check of the data

The loading of boundaries is quite inefficient - I would look to clarify the requirements and perhaps use the CGAZ dataset (https://www.geoboundaries.org/downloadCGAZ.html) or another alternative to avoid multiple look ups
(As an aside have you looked at Snowflake and their data marketplace?)

I would normally load the areas as a separate operation as it is slow and they change infrequently

Option added to the load command to load just ADM3 regions e.g. `docker-compose exec web flask api load_sites --adm3`

I also would normally avoid using a deprecated API i.e. use `https://www.geoboundaries.org/api/current/gbOpen/ALL/ALL/` instead of `https://www.geoboundaries.org/gbRequest.html` however I decided to stick with the URL given in the code/README.md

I kept the response format size quite small and simple but it wouldn't be hard if you wanted to use the same schema as the citybik.es API or add area info

I haven't done any non-functional work such as pinning requirement versions, adding CI/CD, performance management

The tests are limited but check the functional requirements and obvious areas of concern

Add clean target to Makefile to make it easier to start again

Add migrations directory to the docker-compose.yml file to make it easier to access db change scripts (Aware that there are still permission issues since the container is running as root)
 
Modify Makefile to allow creation of migration scripts
    - ```make db-revision ARGS='-m "create sites table"'```
    - Equivalent to ```docker-compose exec web flask db revision -m 'Create sites table'```
