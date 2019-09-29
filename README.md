## TODO app in flask using Flask-SQLAlchemy
[![Build Status](https://travis-ci.com/syamantm/todo-flask.svg?branch=master)](https://travis-ci.com/syamantm/todo-flask)
[![codecov](https://codecov.io/gh/syamantm/todo-flask/branch/master/graph/badge.svg)](https://codecov.io/gh/syamantm/todo-flask)

## Setup

### Setup flask environment
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```



### Setup database

```bash
docker pull postgres
docker run --name some-postgres -e POSTGRES_PASSWORD=postgres -p 5433:5432 -d postgres
```

* This command will start postgres in docker and expose port `5433` for flask application to connect to db
* Now run the database migration

```bash
flask db upgrade
```

## Start server

```bash
flask run
```
Server is now up and running on port 5000(flask default port).

#### test the application !! 

**Create a task** 
```bash
curl -v -X POST -H"content-type:application/json" -d '{"title": "my 1st task from api", "description":"my 1st task from api"}' http://localhost:5000/tasks
```

**Get all tasks**
```bash
curl -v http://localhost:5000/tasks
```

**Get task by id**
```bash
curl -v http://localhost:5000/tasks/1
```

