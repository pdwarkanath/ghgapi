from connect import connect
from psycopg2.extras import RealDictCursor

conn = connect()

MAX_YEAR = 2014
MIN_YEAR = 1990
MAX_ID = 42
MIN_ID = 0
GASES = {'CO2', 'GHGCO2', 'GHG', 'HFC', 'CH4', 'NF3', 'N2O', 'PFC', 'SF6', 'UNSP'}


def is_valid_number(num, min_val, max_val):
    if num.isdigit():
        num = int(num)
        if num < min_val or num > max_val:
            return False
        else:
            return True        
    else:
        return False


def is_valid_gases(gases):
    for gas in gases:
        if gas not in GASES:
            return False
    return True


def get_emissions(event, context):
    if 'id' not in event['params']['path']:
        return {'status': 400, 'body': 'Country id required'}
    else:
        country_id = event['params']['path']['id']
        if is_valid_number(country_id, MIN_ID, MAX_ID):
            country_id = int(country_id)
        else:
            return {'status': 400, 'body': 'Invalid parameter: id'}
    
    if 'startYear' not in event['params']['querystring']:
        start_year = 1990
    else:
        start_year = event['params']['querystring']['startYear']
        if is_valid_number(start_year, MIN_YEAR, MAX_YEAR):
            start_year = int(start_year)
        else:
            return {'status': 400, 'body': 'Invalid parameter: startYear'}
    
    if 'endYear' not in event['params']['querystring']:
        end_year = 2014
    else:
        end_year = event['params']['querystring']['endYear']
        if is_valid_number(end_year, MIN_YEAR, MAX_YEAR):
            end_year = int(end_year)
        else:
            return {'status': 400, 'body': 'Invalid parameter: endYear'}
    
    if start_year > end_year:
        return {'status': 400, 'body': 'Invalid parameters: startYear must be less than endYear'}

    if 'gases' not in event['params']['querystring']:
        gases = tuple(GASES)
    else:
        gases = tuple(event['params']['querystring']['gases'].split('+'))
        if not is_valid_gases(gases):
            return {'status': 400, 'body': 'Invalid parameter: gases'}

    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT country_id as id, year, gas, value FROM emissions WHERE country_id = %s AND gas IN %s AND year BETWEEN %s AND %s', [country_id, gases, start_year, end_year])
    emissions = cur.fetchall()
    return {'status': 200, 'body': emissions}