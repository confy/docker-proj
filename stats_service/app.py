import os
import schedule, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from stats import Stats
from workout import Workout
from pymongo import MongoClient

# Configures SQL
HOST = os.getenv('DB_HOST', 'localhost')
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASSWORD', 'test_pass')
DATABASE = os.getenv('DB_DATABASE', 'proj')
PORT = os.getenv('DB_PORT', 3306)

DB_ENGINE = create_engine("mysql+pymysql://" +
    f"{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}");
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)
print("Connected to MYSQL database.")

# Configures MongoDB
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_USER = os.getenv('MONGO_USER', 'root')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'test_pass')
MONGO_PORT = os.getenv('MONGO_PORT', 27017)
MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'proj')
MONGO_CLIENT= MongoClient('mongodb://' +
    f'{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/?retryWrites=true&w=majority')
MONGO_DB = MONGO_CLIENT[MONGO_DATABASE]
print("Connected to MongoDB database.")


PUBLISH_SECONDS = int(os.getenv('PUBLISH_SECONDS', 5))



def publish_stats() -> None:
    """_summary_
    Calculates statistics for the workouts existent.
    
    Returns:
        Stats: _description_
    """
    print("Running \"publish_stats\"")
    workouts = get_workouts()
    print(workouts)
    if (len(workouts) > 0):
        stats = Stats(workouts)
        MONGO_DB["stats"].insert_one(stats.to_dict())
        print("Calculated stats.")


def get_workouts() -> list:
    """_summary_
    Gets all workouts from the database.
    
    Returns:
        list: _description_

    """
    session = DB_SESSION()
    
    workouts = session.query(Workout).all()
    print(workouts)
    
    session.close()
    
    return workouts

    
        
if __name__ == '__main__':
    print("Starting stats service")
    schedule.every(PUBLISH_SECONDS).seconds.do(publish_stats)
    while 1:
        schedule.run_pending()
        