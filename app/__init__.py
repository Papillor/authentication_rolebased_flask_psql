from flask import Flask
import os
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="bookstore",
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host="localhost",
    port="5432"
)

cur = conn.cursor()

from app import routes