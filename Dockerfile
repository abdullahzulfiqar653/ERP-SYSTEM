# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN ls /code
COPY requirements.txt /code

VOLUME /code
EXPOSE 8000
RUN apt update
RUN pip install psycopg2-binary
RUN apt-get install libpq-dev libxml2-dev libxslt1-dev libssl-dev libffi-dev -y

RUN pip install -r requirements.txt
# RUN chmod 777 /usr/local/bin/docker-entrypoint.sh \
#     && ln -s /usr/local/bin/docker-entrypoint.sh /
COPY . /code/

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# FROM postgres
# ADD init.sql /docker-entrypoint-initdb.d/
