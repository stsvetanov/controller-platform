import sqlite3
from datetime import datetime
import logging


def fill_db(path, parameter):
    conn = None
    time_stamp = datetime.now()
    try:
        conn = sqlite3.connect('flask_app/user_inputs.db')
        cur = conn.cursor()
        split_topic = path.split('/')
        parameter_name = split_topic[2]
        controller_id = split_topic[1]


        sql_query = f'INSERT INTO {parameter_name}(value , time_stamp, controller_id) VALUES (?,?,?)'
        cur.execute(sql_query, [parameter, time_stamp, controller_id])
    except Exception:
        conn.rollback()
        logging.error("Database connection error")
        raise
    else:
        conn.commit()
    finally:
        cur.close()
