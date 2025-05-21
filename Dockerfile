FROM python:3.12

SHELL ["/bin/bash", "-c"]

RUN apt update \
    && apt install -y build-essential curl \
    && apt clean

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"


WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN poetry install

COPY . .



CMD ["poetry", "run", "gunicorn", "home.wsgi:application", "--bind", "0.0.0.0:8000"]