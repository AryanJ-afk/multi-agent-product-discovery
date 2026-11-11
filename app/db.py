import psycopg


def get_connection():
    return psycopg.connect(connect_timeout=5)