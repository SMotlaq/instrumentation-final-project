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
                    user_name TEXT,
                    password_hashed TEXT,
                    name TEXT,
                    parking_number TEXT,
                    isClosed TEXT,
                    credit TEXT
                  ); """
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)
        sql = """ CREATE TABLE IF NOT EXISTS parkings (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    isFull TEXT
                  ); """
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

def add_user(conn, user_name, password_hashed, name, parking_number='0', isClosed='0', credit='0'):
    try:
        sql = ''' INSERT INTO users(user_name, password_hashed, name, parking_number, isClosed, credit)
                  VALUES(?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (user_name, password_hashed, name, parking_number, isClosed, credit,))
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
def query_all_users(conn):
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        link_id = cur.fetchall()
        if link_id==[]:
            return 0
        else:
            return link_id
    except Error as e:
        print(e)
        return 0
def query_all_parkings(conn):
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM parkings')
        link_id = cur.fetchall()
        if link_id==[]:
            return 0
        else:
            return link_id
    except Error as e:
        print(e)
        return 0
def update_user(conn, user_name, password_hashed=None, name=None, parking_number=None, isClosed=None,  credit=None):
    if password_hashed!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET password_hashed=? WHERE user_name=?', (password_hashed, user_name,))
            conn.commit()
        except Error as e:
            print(e)
    if name!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET name=? WHERE user_name=?', (name, user_name,))
            conn.commit()
        except Error as e:
            print(e)
    if parking_number!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET parking_number=? WHERE user_name=?', (parking_number, user_name,))
            conn.commit()
        except Error as e:
            print(e)
    if isClosed!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET isClosed=? WHERE user_name=?', (isClosed, user_name,))
            conn.commit()
        except Error as e:
            print(e)
    if credit!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET credit=? WHERE user_name=?', (credit, user_name,))
            conn.commit()
        except Error as e:
            print(e)
def update_parkings(conn, id, isFull):
    try:
        cur = conn.cursor()
        cur.execute('UPDATE parkings SET isFull=? WHERE id=?', (isFull, id,))
        conn.commit()
    except Error as e:
        print(e)
