FROM python:3.9.6

WORKDIR /app
COPY app.py .

RUN ["pip", "install", "flask"]

EXPOSE 80

CMD [ "python", "app.py" ]