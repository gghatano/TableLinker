# syntax = docker/dockerfile:1.2
FROM python:3.7.5

ENV APP_ROOT=/app
ENV TZ=Asia/Tokyo

# SETUP for app
WORKDIR $APP_ROOT
RUN mkdir /opendata \
  && mkdir -p /run/gunicorn

# Install Poetry
ENV POETRY_HOME=/usr/local
RUN wget --no-check-certificate https://install.python-poetry.org/ -O - | python
ENV PATH=$POETRY_HOME/bin:$PATH

# Install Python Libs
COPY pyproject.toml poetry.lock* $APP_ROOT
RUN poetry config virtualenvs.create false 
RUN --mount=type=cache,target=/root/.cache \
  python -m pip install -U pip setuptools wheel
RUN --mount=type=cache,target=/root/.cache/pypoetry \
  poetry install --no-root --only main

# Launch service
COPY . $APP_ROOT
ENV PORT=8080
CMD python tablelinker/manage.py runserver 0.0.0.0:8000
