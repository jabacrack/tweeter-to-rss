# syntax=docker/dockerfile:1

FROM python:3.6-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY app.py .
COPY twint/twint twint/
COPY twint/requirements.txt requirements2.txt
RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements2.txt

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
