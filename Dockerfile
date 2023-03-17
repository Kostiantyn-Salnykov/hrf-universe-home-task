FROM python:3.9

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME='/usr/local'

RUN mkdir /app

RUN curl -sSL 'https://install.python-poetry.org' | python -
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["make", "update"]
