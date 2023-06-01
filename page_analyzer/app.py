from flask import Flask, request, flash, \
    url_for, redirect, get_flashed_messages, \
    render_template
import os
import requests
from dotenv import load_dotenv
from validators.url import url
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from page_analyzer.use_db import add_url, add_url_check, \
    find_all_checks, find_id_by_name, find_url_by_id, \
    find_url_by_name, get_list_all_url


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
            url=url_input,
            messages=get_flashed_messages(with_categories=True)
        ), 422
    parsed_url = urlparse(url_input)
    corr_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    result = find_url_by_name(corr_url)
    if not result:
        add_url(corr_url)
        flash('Страница успешно добавлена', 'alert-success')
        url_id = find_id_by_name(corr_url)
    else:
        flash('Страница уже существует', 'alert-warning')
        url_id = result.id
    return redirect(url_for('url_info', id=url_id))


@app.route('/urls', methods=['GET'])
def all_urls():
    urls = get_list_all_url()
    return render_template('all_urls.html', urls=urls)


@app.route('/urls/<int:id>', methods=['GET'])
def url_info(id):
    url = find_url_by_id(id)
    checks = find_all_checks(id)
    if url is None:
        flash('Такой страницы не существует', 'alert-warning')
        return redirect(url_for('index'))
    return render_template('show_details.html', id=id, name=url.name,
                           created_at=url.created_at,
                           checks=checks
                           )


@app.route('/urls/<id>/checks', methods=['POST'])
def url_checks(id):
    url = find_url_by_id(id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return redirect(url_for('url_info', id=id))
    status = response.status_code
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.h1.get_text() if soup.h1 else ''
    title = soup.title.get_text() if soup.title else ''
    descr = soup.find('meta', {'name': 'description'})
    description = descr['content'] if descr else ''
    add_url_check(id, status, h1, title, description)
    flash('Страница успешно проверена', 'alert-success')
    return redirect(url_for('url_info', id=id))
