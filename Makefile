install:

		poetry install

test-coverage:
	
		poetry run pytest --cov=page_analyzer --cov-report xml

dev:

		poetry run flask --app page_analyzer:app run

lint:

		poetry run flake8 .

PORT ?= 8000
start:

		poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
