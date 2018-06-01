import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
 
 
def select_all(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
	#cur.execute("INSERT INTO test VALUES(?, ?)", ("C", 3))
    cur.execute("SELECT * FROM test")
    rows = cur.fetchall()
    for row in rows:
    	print(row)

def insert_db(conn, val1, val2):
    curr = conn.cursor();
    curr.execute("INSERT INTO TEST VALUES (?, ?)", (val1, val2))

def main():
    database = "test.db"
    #value = input("Enter the tuple you want entered: ")
    val1, val2 = input("Enter the tuple you want entered: ").split()
    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT load_extension('mod-spatialite')")
    cur.execute("SELECT InitSpatialMetaData()")
    # insert_db(conn, val1, val2);
    # with conn:
    #     select_all(conn)
 
 
if __name__ == '__main__':
    main()