import sqlite3
from sqlite3 import Error
import numpy.matlib as npm
import os

db_address = os.path.dirname(os.path.abspath(__file__)) + '\database.db'

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread = False)
    except Error as e:
        print(e)
    return conn


def delete_all_rows_from_link_table(conn,src,dest):
    if conn is not None:
        sql = " DELETE FROM {}_to_{} ".format(src,dest)
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)


def create_table(conn):
    if conn is not None:
        sql = """ CREATE TABLE IF NOT EXISTS nodes (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    name text,
                    type text,
                    position_x float,
                    position_y float
                  ); """
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)
    
def add_nodes(conn, node):
    try:
        sql = ''' INSERT INTO nodes(name, type, position_x, position_y)
                  VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, node)
        print('hy')
        return cur.lastrowid
    except Error as e:
        print(e)

def add_links(conn, link):
    sql = ''' INSERT INTO links(name, type, alpha_index, gamma_index, beta1_index, beta2_index, beta3_index, D_index, gain, distance, source, destination)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, link)
    return cur.lastrowid

def delete_node(conn, id):
    #------------------------------delete connected links------------------------------
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM links WHERE source=? OR destination=?', (id,id,))
        conn.commit()
    except Error as e:
        print(e)
    
    #-------------------------correct source & destination IDs-------------------------
    try:
        cur = conn.cursor()
        cur.execute('UPDATE links SET source=source-1 WHERE source>?', (id,))
        conn.commit()
    except Error as e:
        print(e)

    try:
        cur = conn.cursor()
        cur.execute('UPDATE links SET destination=destination-1 WHERE destination>?', (id,))
        conn.commit()
    except Error as e:
        print(e)
    #------------------------------------delete node-----------------------------------
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM nodes WHERE id=?', (id,))
        conn.commit()
    except Error as e:
        print(e)
    #----------------------------------resort node IDs---------------------------------    
    try:
        cur = conn.cursor()
        cur.execute('UPDATE nodes SET id=id-1 WHERE id>?', (id,))
        conn.commit()
    except Error as e:
        print(e)

def delete_link(conn, id):
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM links WHERE id=?', (id,))
        conn.commit()
    except Error as e:
        print(e)

def max_node_id(conn):
    try:    
        cur = conn.cursor()
        cur.execute('SELECT MAX(id) FROM nodes')
        row = cur.fetchall()
        return row[0][0]
    except Error as e:
        print(e)
        return 0

def query_link_id(conn, source, destination):
    try:
        cur = conn.cursor()
        cur.execute('SELECT id FROM links WHERE source=? AND destination=?', (source, destination,))
        link_id = cur.fetchall()
        if link_id==[]:
            return 0
        else:
            return link_id[0][0]
    except Error as e:
        print(e)
        return 0

def make_matrix(conn):
    matrix_size = max_node_id(conn)
    out = npm.zeros((matrix_size,matrix_size))
    for row in range(matrix_size):
        for column in range(matrix_size):
            out[row,column] = query_link_id(conn, column+1, row+1)
    return out+out.transpose()

def update_node_properties(conn, id, newName=None, newType=None, newX=None, newY=None):
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE nodes SET name=? WHERE id=?', (newName,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newType is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE nodes SET type=? WHERE id=?', (newType,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newX is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE nodes SET position_x=? WHERE id=?', (newX,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newY is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE nodes SET position_y=? WHERE id=?', (newY,id,))
            conn.commit()
        except Error as e:
            print(e)

def update_link_properties(conn, id, newName=None, newType=None, newAlphaIndex=None, 
                           newGammaIndex=None, newBetaIndex1=None, newBetaIndex2=None, 
                           newBetaIndex3=None, newDIndex=None, newGain= None, 
                           newDistance=None, newSource=None, newDestination=None):
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET name=? WHERE id=?', (newName,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET type=? WHERE id=?', (newType,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET alpha_index=? WHERE id=?', (newAlphaIndex,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET gamma_index=? WHERE id=?', (newGammaIndex,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET beta1_index=? WHERE id=?', (newBetaIndex1,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET beta2_index=? WHERE id=?', (newBetaIndex2,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET beta3_index=? WHERE id=?', (newBetaIndex3,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET D_index=? WHERE id=?', (newDIndex,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET gain=? WHERE id=?', (newGain,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET distance=? WHERE id=?', (newDistance,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET source=? WHERE id=?', (newSource,id,))
            conn.commit()
        except Error as e:
            print(e)
    if newName is not None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE links SET destination=? WHERE id=?', (newDestination,id,))
            conn.commit()
        except Error as e:
            print(e)


def create_results_table(conn, node_num):
    if conn is not None:
        sql = "DROP TABLE IF EXISTS results;"
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)
        sql = """ CREATE TABLE IF NOT EXISTS results (
                    id integer,
                    source text,
                    destination text,
                    type text,
                    wavelengthIndex integer,
                    OSNR float,
                    length float, 
                    protOSNR float, 
                    protLength float
                  ); """
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

        for num in range(node_num):  # main path nodes
            num = num + 1
            sql = "ALTER TABLE results ADD COLUMN '{}' text".format(str(num))
            try:
                c = conn.cursor()
                c.execute(sql)
            except Error as e:
                print(e)
        for num in range(node_num):  # protection path nodes
            num = num + 1
            sql = "ALTER TABLE results ADD COLUMN '{}' text".format(str(num+100))
            try:
                c = conn.cursor()
                c.execute(sql)
            except Error as e:
                print(e)
        for num in range(node_num):  # main path regenerators
            num = num + 1
            sql = "ALTER TABLE results ADD COLUMN '{}' text".format(str(num+200))
            try:
                c = conn.cursor()
                c.execute(sql)
            except Error as e:
                print(e)
        for num in range(node_num):  # protection path regenerators
            num = num + 1
            sql = "ALTER TABLE results ADD COLUMN '{}' text".format(str(num+300))
            try:
                c = conn.cursor()
                c.execute(sql)
            except Error as e:
                print(e)
    else:
        print('Error: cannot connect to database')
