import connexion
import os
import flask
import sys
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

}

DB_ENGINE = create_engine(
    f"mysql+pymysql://{conf['user']}:{conf['password']}@{conf['host']}:{conf['port']}/{conf['db']}")

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def authenticate(body):
    auth_body = {
        "username": body["username"],
        "password": body["password"]
    }
    r = requests.post(
        f"http://{conf['auth_host']}/", json=auth_body)
    return r.status_code == 200


def post_workout(body):
    """Authorize credentials and add a new workout if valid credentials are provided"""
    try:
        logged_in = authenticate(body)
        if not logged_in:
            print("Invalid credentials", file=sys.stderr)
            return "Invalid Input", 405

        workout = Workout(
            body['workout']["start_timestamp"],
            body['workout']["end_timestamp"],
            body['workout']["minimum_heart_rate"],
            body['workout']["peak_heart_rate"],
            body['workout']["calories_burned"]
        )
        session = DB_SESSION()
        session.add(workout)
        session.commit()
        return NoContent, 201
    except Exception as e:
        print(e, file=sys.stderr)
        return "Invalid Input", 405


def get_index():
    return flask.send_from_directory('www', 'index.html')

def get_app_js():
    return flask.send_from_directory('www', 'app.js')

options = {"swagger_ui": False}
app = connexion.FlaskApp(__name__, specification_dir='', options=options)
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
