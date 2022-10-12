import connexion
import os
import flask
import requests


from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.base import Base
from src.workout import Workout

conf = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "db": os.getenv("DB_DATABASE"),
    "auth_host": os.getenv("AUTH_HOST"),
    "auth_port": os.getenv("AUTH_PORT")
}

DB_ENGINE = create_engine(
    f"mysql+pymysql://{conf['user']}:{conf['password']}@{conf['host']}:{conf['port']}/{conf['db']}")

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def get_index():
    return flask.send_from_directory('www', 'index.html')


def post_workout(body):
    """Authorize credentials and add a new workout if valid credentials are provided"""
    r = 
    return body, 201


options = {"swagger_ui": False}
app = connexion.FlaskApp(__name__, specification_dir='', options=options)
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)
