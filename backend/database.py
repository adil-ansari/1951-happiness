import psycopg2
from psycopg2.extras import RealDictCursor

def get_db():
    conn = psycopg2.connect(host='localhost', dbname='1951-happiness', user='postgres', password='admin', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()
        conn.close()
