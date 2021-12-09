from connect import connect
import json
from psycopg2.extras import RealDictCursor

conn = connect()

MAX_YEAR = 2014
MIN_YEAR = 1990
gases = {'CO2', 'GHGCO2', 'GHG', 'HFC', 'CH4', 'NF3', 'N2O', 'PFC', 'SF6', 'UNSP'}

def clean_gases(gases):
    return

def clean_year(year):
    return

def get_emissions(event, context):
    country_id = int(event['path'][len('/country/'):])
    start_year = int(event['queryStringParameters']['startYear'])
    end_year = int(event['queryStringParameters']['endYear'])
    gases = tuple(event['queryStringParameters']['gases'].split('+'))
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT country_id as id, year, gas, value FROM emissions WHERE country_id = %s AND gas IN %s AND year BETWEEN %s AND %s', [country_id, gases, start_year, end_year])
    emissions = cur.fetchall()
    return json.dumps(emissions)