import mysql.connector
import os

HOST = os.getenv('DB_HOST', 'localhost')
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASS', 'test_pass')
DATABASE = os.getenv('DB_DATABASE', 'proj')

db_conn = mysql.connector.connect(host=HOST,
    user='root', password=PASSWORD, database=DATABASE)
print(f"Connected to \"{DATABASE}\" database on \"{HOST}\" as \"{USER}\"")

c = db_conn.cursor();

try:
    c.execute('''
            DROP TABLE workout
            ''');
    print('Dropped table workout.')
except:
    print('Table workout does not exist.')

c.execute('''
          CREATE TABLE workout
          (id INT NOT NULL AUTO_INCREMENT,
           start_timestamp VARCHAR(100) NOT NULL,
           end_timestamp VARCHAR(100) NOT NULL,
           minimum_heart_rate INT NOT NULL,
           peak_heart_rate INT NOT NULL,
           calories_burned INT NOT NULL,
           CONSTRAINT workout_pk PRIMARY KEY (id))
          ''');
print('Created table workout.')

db_conn.commit();
db_conn.close();