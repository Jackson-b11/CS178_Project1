import pymysql
import pymysql.cursors
import creds
import boto3

# Establish connection with RDS provided
def get_conn():

    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )

# Function that takes query and args and using get_conn function above returns the results of a query
def execute_query(query,args=()):

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query,args)
            rows=cur.fetchall()
        return rows
    finally:
        conn.close()

# Function used in flaskappv1.py
def show_country():
    query = """
        SELECT country.name AS name, 
               country.lifeexpectancy AS lifeexpectancy, 
               countrylanguage.language AS language
        FROM country
        JOIN countrylanguage ON country.code = countrylanguage.countrycode
        LIMIT 5;
    """
    return execute_query(query)






