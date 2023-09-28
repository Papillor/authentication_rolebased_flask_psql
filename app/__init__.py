from flask import Flask
import os
import psycopg2

app = Flask(__name__)

app.secret_key = 'root'

conn = psycopg2.connect(
    dbname="rbacauth",
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host="localhost",
    port="5432"
)

cur = conn.cursor()

from app.routes import auth
from app.routes import crud