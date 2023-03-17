# === Linter's commands ===
black:
	poetry run black . $(args)

lint:
	poetry run flake8 $(args)

isort:
	poetry run isort . $(args)

fmt: black isort lint

# === Back-end commands ===
migrate:
	poetry run alembic upgrade head

run:
	poetry run gunicorn main:app -c gunicorn.conf.py

run_uvicorn:
	python -m main

update: migrate run
