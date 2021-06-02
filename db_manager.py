import sqlite3


def create_connection(db_file):
    """ (string) --> Connection object
    Create a database connection to a SQLite database

    db_file: database file name
    return: Connection object [sqlite3]"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print("Connection Established")
        return conn
    except sqlite3.Error as e:
        print(e)
    
    return conn

def create_table(conn, create_table_sql):
    """ (Connection object, string) --> None
    Create a table from the create_table_sql statement
    
    conn: Connection object [sqlite3]
    create_table_sql: a CREATE TABLE statement
    return: None
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
        #print("Database written")
    except sqlite3.Error as e:
        print(e)


def insert_message(conn, values):
    """(Connection object, tuple) --> None
    Insert a new row into the id_to_file table
    
    conn: Connection object [sqlite3]
    values: tuple of string
    return: None
    """
    sql = ''' INSERT INTO id_to_file(Message_Id, File_Path)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, values)
    #print("Row inserted")

def delete_message(conn, id):
    """ (Connection object, int) --> string
    Delete a row into from the id_to_file
    table by message id

    conn: Connection object [sqlite3]
    id: message id [telethon]
    return: file path
    """
    cur = conn.cursor()
    sql1 = "SELECT File_Path FROM id_to_file WHERE Message_Id=?"
    sql2 = "DELETE FROM id_to_file WHERE Message_Id=?"
    cur.execute(sql1, (id,))
    file_path = cur.fetchone()
    if not file_path:
        return ""
    cur.execute(sql2, (id,))
    conn.commit()
    #print("Row Deleted")
    return file_path[0]