# syntax=docker/dockerfile:1

FROM python:3.9.13

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["gunicorn", "-c", "gunicorn_config.py", "app:app"]