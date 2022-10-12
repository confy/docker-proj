import os
from sqlalchemy import create_engine
from sqlalchemy import sessionmaker
from base import Base
from stats import Stats
from workout import Workout
from apscheduler.schedulers.background import BackgroundScheduler

DATABASE = os.getenv('DB_DATABASE', 'proj')
HOSTNAME = os.getenv('DB_HOST', 'localhost')
PORT = os.getenv('DB_PORT', 3306)
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASS', 'password')
PUBLISH_SECONDS = os.getenv('PUBLISH_SECONDS', 5)

DB_ENGINE = create_engine("mysql+pymysql://" +
    f"{USER}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}");

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def publish_stats() -> Stats:
    """_summary_
    Calculates statistics for the workouts existent.
    
    Returns:
        Stats: _description_
    """
    workouts = get_workouts()
    stats = Stats(workouts)


def get_workouts() -> list:
    """_summary_
    Gets all workouts from the database.
    
    Returns:
        list: _description_

    """
    session = DB_SESSION()
    
    workouts = session.query(Workout).all()
    
    session.close()
    
    return workouts
    
    
def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(publish_stats,
        'interval',
        seconds=PUBLISH_SECONDS)
    sched.start()
    
    
if __name__ == '__main__':
    init_scheduler()