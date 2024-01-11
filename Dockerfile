# Use an official Python runtime as a parent image
FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/wait-for-postgresql.sh

EXPOSE 53012

ENTRYPOINT ["/app/entrypoint.sh"]
