import sqlite3
from sqlite3 import Error

def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)

	return None

def select_all(conn):
	cur = conn.cursor()
	cur.execute("INSERT INTO test VALUES(?, ?)", ("C", 3))
	cur.execute("SELECT * FROM test")
	rows = cur.fetchall()
	for row in rows:
		print(row)

	cur.execute("DELETE FROM test WHERE test.num = 3")

def main():
	database = "test.db"

	conn = create_connection(database)
	with conn:
		select_all(conn)

if __name__ == '__main__':
	main()