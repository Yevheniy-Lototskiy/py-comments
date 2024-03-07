FROM python:3.11-slim-bullseye
LABEL maintainer="yevhenii.lototskyi@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR comments/

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

USER django-user
