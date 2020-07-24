import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread = False)
    except Error as e:
        print(e)
    return conn
def create_table(conn):
    if conn is not None:
        sql = """ CREATE TABLE IF NOT EXISTS users (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    uwer_name text,
                    password_hashed text,
                    name text,
                    parking_number text,
                    credit text
                  ); """
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

def add_user(conn, user_name, password_hashed, name, parking_number=None, credit='0'):
    try:
        sql = ''' INSERT INTO users(user_name, password_hashed, name, parking_number, credit)
                  VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (user_name, password_hashed, name, parking_number, credit,))
        return cur.lastrowid
    except Error as e:
        print(e)
def query_user(conn, user_name):
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE user_name=?', (user_name,))
        link_id = cur.fetchall()
        if link_id==[]:
            return 0
        else:
            return link_id[0]
    except Error as e:
        print(e)
        return 0
def update_user(conn, user_name, password_hashed=None, name=None, parking_number=None, credit=None):
    if password_hashed is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET password_hashed=? WHERE user_name=?', (password_hashed, user_name,))
            conn.commit()
        except Error as e:
            print(e)
    if name is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET name=? WHERE user_name=?', (name, user_name,))
            conn.commit()
        except Error as e:
            print(e)
    if parking_number is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET parking_number=? WHERE user_name=?', (parking_number, user_name,))
            conn.commit()
        except Error as e:
            print(e)
    if credit is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET credit=? WHERE user_name=?', (credit, user_name,))
            conn.commit()
        except Error as e:
            print(e)
