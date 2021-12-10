from connect import connect

from psycopg2.extras import RealDictCursor

conn = connect()

def get_countries(event, context):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT id, country, start_year AS startYear, end_year AS endYear FROM countries')
    countries = cur.fetchall()
    return countries
