# Use an official Python runtime as a parent image
FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 53012

CMD ["alembic", "upgrade", "head", "&&", "python", "-m", "scripts.SetupDatabase", "&&", "hypercorn", "main:app", "--bind", "0.0.0.0:53012"]
