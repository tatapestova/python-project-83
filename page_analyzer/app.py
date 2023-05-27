from flask import Flask, request, flash, \
    url_for, redirect, get_flashed_messages, \
    render_template
import psycopg2
from psycopg2.extras import NamedTupleCursor
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from validators.url import url
from urllib.parse import urlparse
from bs4 import BeautifulSoup


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET = os.environ.get('SECRET_KEY')


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def urls_post():
    data_input = request.form.to_dict()
    url_input = data_input.get('url')
    if url(url_input) is not True:
        flash('Некорректный URL', 'alert-danger')
        if not url_input:
            flash('URL обязателен', 'alert-danger')
        return render_template(
            'index.html',
            url=data_input,
            messages=get_flashed_messages(with_categories=True)
        ), 422
    parsed_url = urlparse(url_input)
    corr_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute("SELECT * FROM urls WHERE name = %s",
                (corr_url, ))
    result = cur.fetchone()
    if not result:
        cur.execute("INSERT INTO urls (name, created_at) \
                    VALUES (%s, %s)", (corr_url, datetime.now()))
        conn.commit()
        flash('Страница успешно добавлена', 'alert-success')
        cur.execute("SELECT id FROM urls WHERE name = %s", (corr_url, ))
        url_info = cur.fetchone()
        url_id = url_info.id
        conn.close()
    else:
        flash('Страница уже существует', 'alert-warning')
        conn.close()
        url_id = result.id
    return redirect(url_for('url_info', id=url_id))


@app.route('/urls', methods=['GET'])
def all_urls():
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
    return render_template('all_urls.html', urls=urls)


@app.route('/urls/<int:id>', methods=['GET'])
def url_info(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s",
                    (id,))
        url = cur.fetchone()
        cur.execute("SELECT * FROM  url_checks WHERE url_id = %s \
                    ORDER BY created_at DESC",
                    (id,))
        checks = cur.fetchall()
    if url is None:
        flash('Такой страницы не существует', 'alert-warning')
        return redirect(url_for('index'))
    return render_template('show_details.html', id=id, name=url.name,
                           created_at=url.created_at,
                           checks=checks
                           )


@app.route('/urls/<id>/checks', methods=['POST'])
def url_checks(id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute("SELECT name from urls WHERE id = %s", (id, ))
    url = cur.fetchone()
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        conn.close()
        flash('Произошла ошибка при проверке', 'alert-danger')
        return redirect(url_for('url_info', id=id))
    status = response.status_code
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.h1.string if soup.h1.string else ''
    title = soup.title.string if soup.title.string else ''
    descr = soup.find('meta', {'name': 'description'})
    description = descr['content'] if descr else ''
    cur.execute("INSERT INTO url_checks ( \
                url_id, created_at, status_code, h1, title, description) \
                VALUES (%s, %s, %s, %s, %s, %s)", (
                id, datetime.now(), status, h1, title, description))
    conn.commit()
    flash('Страница успешно проверена', 'alert-success')
    conn.close()
    return redirect(url_for('url_info', id=id))
