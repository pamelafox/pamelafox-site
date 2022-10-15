# syntax=docker/dockerfile:1

FROM python:3.10.8

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["gunicorn", "-c", "gunicorn_config.py", "--workers", "1", "app:app"]