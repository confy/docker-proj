import mysql.connector
import os

HOST = os.getenv('HOST', 'localhost')
USER = os.getenv('USER', 'root')
PASSWORD = os.getenv('PASSWORD', 'password')
DATABASE = os.getenv('DATABASE', 'proj')

db_conn = mysql.connector.connect(host=HOST,
    user='root', password=PASSWORD, database=DATABASE)

c = db_conn.cursor();
c.execute('''
          CREATE TABLE workout
          (id INT NOT NULL AUTO_INCREMENT,
           start_timestamp VARCHAR(100) NOT NULL,
           end_timestamp VARCHAR(100) NOT NULL,
           CONSTRAINT train_arrival_pk PRIMARY KEY (id))
          ''');

db_conn.commit();
db_conn.close();