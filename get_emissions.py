from connect import connect
import json
from psycopg2.extras import RealDictCursor

conn = connect()

def get_emissions(event, context):
    country_id = 3
    start_year = 1995
    end_year = 2013
    gases = ('CO2',)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT country_id as id, year, gas, value FROM emissions WHERE country_id = %s AND gas IN %s AND year BETWEEN %s AND %s', [country_id, gases, start_year, end_year])
    emissions = cur.fetchall()
    return json.dumps(emissions)