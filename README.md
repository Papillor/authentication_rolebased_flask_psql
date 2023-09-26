# Authentication with roles

## Setting up

### Venv

```bash
# create a venv

python3 -m venv "nameofyourvenv"

# activate a venv

source myenv/bin/activate
```

### Postgres

```psql
# create the db

CREATE DATABASE bookstore;
GRANT ALL PRIVILEGES ON DATABASE bookstore TO youruser;

# select the db

\c bookstore;

# to connect to database

psql -U youruser yourdb

# to populate the database 

export POSTGRES_USER='youruser'
export POSTGRES_PASSWORD='yourpassword'

python3 init_db.py
```

## Documentation

- https://flask-user.readthedocs.io/en/latest/index.html
