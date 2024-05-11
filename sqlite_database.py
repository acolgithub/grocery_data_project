import sqlite3


# create database file
def create_sqlite_database(filename):

    # create connection
    conn = None

    try:

        # create database file and connect to it
        conn = sqlite3.connect(filename)

        # print version if successful
        print(sqlite3.sqlite_version)

    except sqlite3.Error as e:

        # if connection fails to form print error message
        print(e)

    finally:

        # if conenction was formed close connection
        if conn:

            conn.close()


# define function to add data to reddit database
def add_data(conn, data: list[str]) -> None:

    # form SQL statement to add data
    sql = """INSERT INTO reddit_data(subreddit, description, link, permalink)
              VALUES(?, ?, ?, ?)""" 
    
    # get cursor
    cur = conn.cursor()

    # execute sql statement
    cur.execute(sql, data)

    # commit transaction
    conn.commit()

    return cur.lastrowid


# define function to execute statement
def execute_statement(conn, statement):

    # get cursor
    cur = conn.cursor()

    # execute statement
    cur.execute(statement)

    # fetch result
    output = cur.fetchall()

    # print each row of output
    for row in output:
        print(row)

    # commit connection
    conn.commit()











