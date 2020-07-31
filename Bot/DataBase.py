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
                    uid text,
                    name text,
                    user_id text,
                    p_user_name text,
                    p_password text,
                    parking_number text,
                    time text,
                    state text
                  ); """
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

def add_user(conn, uid, name, user_id, p_user_name=None, p_password=None, parking_number=None, time=None, state=None):
    try:
        sql = ''' INSERT INTO users(uid, name, user_id, p_user_name, p_password, parking_number, time, state)
                  VALUES(?,?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (uid, name, user_id, p_user_name, p_password, parking_number, time, state,))
        return cur.lastrowid
    except Error as e:
        print(e)
def query_user(conn, uid):
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE uid=?', (uid,))
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
def update_user(conn, uid, name=None, user_id=None, p_user_name=None, p_password=None, parking_number=None, time=None, state=None):
    if name is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET name=? WHERE uid=?', (name, uid,))
            conn.commit()
        except Error as e:
            print(e)
    if user_id is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET user_id=? WHERE uid=?', (user_id, uid,))
            conn.commit()
        except Error as e:
            print(e)
    if p_user_name is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET p_user_name=? WHERE uid=?', (p_user_name, uid,))
            conn.commit()
        except Error as e:
            print(e)
    if p_password is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET p_password=? WHERE uid=?', (p_password, uid,))
            conn.commit()
        except Error as e:
            print(e)
    if parking_number is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET parking_number=? WHERE uid=?', (parking_number, uid,))
            conn.commit()
        except Error as e:
            print(e)
    if time is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET time=? WHERE uid=?', (time, uid,))
            conn.commit()
        except Error as e:
            print(e)
    if time is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET time=? WHERE uid=?', (time, uid,))
            conn.commit()
        except Error as e:
            print(e)
    if state is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET state=? WHERE uid=?', (state, uid,))
            conn.commit()
        except Error as e:
            print(e)
