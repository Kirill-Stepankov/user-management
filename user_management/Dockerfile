FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry==1.6.1

COPY ../pyproject.toml poetry.lock  ./
COPY ./localstack-script.sh ./

RUN chmod +x ./localstack-script.sh

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /app/
