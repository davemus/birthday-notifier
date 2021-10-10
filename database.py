import os
import atexit
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
# singletones, because practicability beats purity
connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()


def cleanup():
    cursor.close()
    connection.close()

atexit.register(cleanup)

