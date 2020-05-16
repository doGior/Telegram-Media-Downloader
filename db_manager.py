import sqlite3


def create_connection(db_file):
    """ Create a database connection to a SQLite database
    db_file: database file name
    return: Connection object """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection Established")
        return conn
    except sqlite3.Error as e:
        print(e)
    
    return conn

def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement
    param conn: Connection object
    param create_table_sql: a CREATE TABLE statement
    return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
        #conn.close()
        print("Database written - SQLite version",sqlite3.version)
    except sqlite3.Error as e:
        print(e)


def insert_message(conn, values):
    """
    Insert a new row into the id_to_file table
    conn: Connection object
    values: tuple of string
    return: table id
    """
    sql = ''' INSERT INTO id_to_file(Message_Id, File_Path)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, values)
    return cur.lastrowid


def delete_message(conn, id):
    """
    Delete a row into from the id_to_file
    table by message id
    conn: Connection object
    id: message id
    return: table id
    """
    sql1 = "SELECT File_Path FROM id_to_file WHERE Message_Id=?"
    sql2 = "DELETE FROM id_to_file WHERE Message_Id=?"
    cur = conn.cursor()
    cur.execute(sql1, (id,))
    file_path = cur.fetchone()[0]
    cur.execute(sql2, (id,))
    conn.commit()
    print("Row Deleted")
    return file_path

