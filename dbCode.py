import pymysql
import pymysql.cursors
import creds
import boto3

def get_conn():

    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )

def execute_query(query,args=()):

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query,args)
            rows=cur.fetchall()
        return rows
    finally:
        conn.close()


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






