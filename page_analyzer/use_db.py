from datetime import datetime
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import NamedTupleCursor


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET = os.environ.get('SECRET_KEY')


def find_url_by_name(url):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute("SELECT * FROM urls WHERE name = %s",
                (url, ))
    result = cur.fetchone()
    conn.close()
    return result


def add_url(url):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute("INSERT INTO urls (name, created_at) \
                    VALUES (%s, %s)", (url, datetime.now()))
    conn.commit()
    conn.close()


def find_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute("SELECT * FROM urls WHERE id = %s",
                (id, ))
    result = cur.fetchone()
    conn.close()
    return result


def find_id_by_name(url):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute("SELECT id FROM urls WHERE name = %s", (url, ))
    url_info = cur.fetchone()
    url_id = url_info.id
    conn.close()
    return url_id


def get_list_all_url():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute("SELECT urls.id, urls.name, \
                MAX(url_checks.created_at) AS check_time, \
                url_checks.status_code FROM urls \
                LEFT JOIN url_checks \
                ON urls.id = url_checks.url_id \
                GROUP BY urls.id, urls.name, url_checks.status_code \
                ORDER BY urls.id DESC;"
                )
    urls = cur.fetchall()
    conn.close()
    return urls


def find_all_checks(id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute("SELECT * FROM  url_checks WHERE url_id = %s \
                ORDER BY created_at DESC",
                (id,))
    checks = cur.fetchall()
    conn.close()
    return checks


def add_url_check(id, status, h1, title, description):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute("INSERT INTO url_checks ( \
                url_id, created_at, status_code, h1, title, description) \
                VALUES (%s, %s, %s, %s, %s, %s)", (
                id, datetime.now(), status, h1, title, description))
    conn.commit()
    conn.close()
