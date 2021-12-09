import psycopg2
import json
import os

username = os.eniron['username']
password = os.eniron['password']

conn = psycopg2.connect(
    host="ghgapi.cap6ippkvuoh.us-east-2.rds.amazonaws.com",
    database="ghgapi",
    user=username,
    password=password)

def get_countries(event, context):
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT id, country, start_year AS startYear, end_year AS endYear FROM countries')
    countries = cur.fetchall()
    return json.dumps(countries)
