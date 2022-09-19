# Hanzels Todo
## Prerequisites
Make sure python 3.10 is installed
### Poetry
This project is made using poetry packet manager so make sure it is available on your system
```
pip install poetry
```
After cloning this repo, cd into the root directory and run
```
poetry shell
poetry install
```

### Environment variables
The project makes use of environment variables for configuration. One way to do this is to provide a ".env" file in the root of project directory with the following contents
```
PERSISTENCY=memory # memory / sqllite / mongo
```
If SQLite is available on your sysstem you can use sqllite as PERSISTENCY environment variable  
Mongo persistency is yet to be implemented

## How to run
### Start the application
```
poetry run start
```

### Testing the backend routes
```bash
# List all todo's
curl --request GET --url http://localhost:5000/todo
# Get todo by id
curl --request GET --url http://localhost:5000/todo/00000000-0000-0000-0000-000000000001
# Create todo
curl --request POST --url http://localhost:5000/todo --header 'Content-Type: application/json' --data '{ "text": "Tuduuuum! A brand new one" }'
# Update todo
curl --request PUT \
  --url http://localhost:5000/todo \
  --header 'Content-Type: application/json' \
  --data '{
	"create_time": "Mon, 19 Sep 2022 10:18:48 GMT",
	"id": "00000000-0000-0000-0000-000000000003",
	"resolve_time": null,
	"status": 0,
	"text": "Maybe better not eat MC Donalds"
}'
# Delete todo
curl --request DELETE \
  --url http://localhost:5000/todo/00000000-0000-0000-0000-000000000001
```

### Very basic UI
The index route (http://localhost:5000/) of the application provides you with a very basic ui, no frameworks used here and this still needs to be fleshed out