# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=groupsremover.settings \
    PORT=8000 \
    WEB_CONCURRENCY=3
RUN addgroup --system django \
    && adduser --system --ingroup django django
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt install -y gcc
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput --clear
RUN chown -R django:django /app
USER django
CMD gunicorn groupsremover.wsgi:application
