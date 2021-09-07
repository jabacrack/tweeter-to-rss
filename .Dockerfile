# syntax=docker/dockerfile:1

FROM jabacrack/flask-and-twint:1.1

WORKDIR /app

COPY app.py .

EXPOSE 80

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]
