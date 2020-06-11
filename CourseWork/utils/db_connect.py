import mysql.connector

def db_connect(us: str, passw: str, hst: str, db: str):
    try:
        conn = mysql.connector.connect(user = us,
                                       password = passw,
                                       host = hst,
                                       database = db)
    except:
        conn = None

    return conn
