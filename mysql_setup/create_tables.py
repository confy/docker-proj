import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

HOST = os.getenv('DB_HOST', 'localhost')
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASSWORD', 'test_pass')
DATABASE = os.getenv('DB_DATABASE', 'proj')
PORT = os.getenv('DB_PORT', 3306)

DB_ENGINE = create_engine("mysql+pymysql://" +
    f"{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}");

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

print(f"Connected to \"{DATABASE}\" database on \"{HOST}\" as \"{USER}\"")

try:
    with DB_ENGINE.connect() as con:
        rs = con.execute('''
            DROP TABLE workout
            ''')
        print('Dropped table workout.')
except:
    print('Table workout does not exist.')

with DB_ENGINE.connect() as con:
    rs = con.execute('''
          CREATE TABLE workout
          (id INT NOT NULL AUTO_INCREMENT,
           start_timestamp VARCHAR(100) NOT NULL,
           end_timestamp VARCHAR(100) NOT NULL,
           minimum_heart_rate INT NOT NULL,
           peak_heart_rate INT NOT NULL,
           calories_burned INT NOT NULL,
           CONSTRAINT workout_pk PRIMARY KEY (id))
          ''')
    print('Created table workout.')