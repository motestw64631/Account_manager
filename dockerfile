FROM python:3.9.19-slim-bullseye

WORKDIR /code
RUN apt-get update && apt-get install -y netcat

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini
COPY ./app /code/app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

