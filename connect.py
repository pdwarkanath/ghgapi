import psycopg2
import os

username = os.environ['username']
password = os.environ['password']

def connect():
    conn = psycopg2.connect(
        host="ghgapi.cap6ippkvuoh.us-east-2.rds.amazonaws.com",
        database="ghgapi",
        user=username,
        password=password)
    return conn