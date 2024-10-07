import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='',  
            database='senatus'  
        )
        if connection.is_connected():
            print("Successfully connected to the database")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection

def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS decisions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE NOT NULL,
        meeting_number INT NOT NULL,
        decision TEXT NOT NULL,
        president VARCHAR(255) NOT NULL,
        secretary VARCHAR(255) NOT NULL
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


    cursor = connection.cursor()
    select_query = "SELECT * FROM decisions"
    
    try:
        cursor.execute(select_query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except Error as e:
        print(f"The error '{e}' occurred")


    cursor = connection.cursor()
    select_query = "SELECT * FROM decisions"
    
    try:
        cursor.execute(select_query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except Error as e:
        print(f"The error '{e}' occurred")
def drop_table(connection, table_name):
    cursor = connection.cursor()
    drop_query = f"DROP TABLE IF EXISTS {table_name};"
    try:
        cursor.execute(drop_query)
        connection.commit()
        print(f"A(z) {table_name} tábla sikeresen törölve.")
    except Exception as e:
        print(f"Hiba a tábla törlésekor: {e}")

def create_tables(connection):
    cursor = connection.cursor()

    create_meetings_table = """
    CREATE TABLE IF NOT EXISTS meetings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_number VARCHAR(255) NOT NULL,
        date DATE NOT NULL,
        president VARCHAR(255) NOT NULL,
        secretary VARCHAR(255) NOT NULL
    );
    """

    create_resolutions_table = """
    CREATE TABLE IF NOT EXISTS resolutions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        meeting_id INT NOT NULL,
        resolution_number INT NOT NULL,
        content TEXT NOT NULL,
        appendix VARCHAR(255),
        FOREIGN KEY (meeting_id) REFERENCES meetings(id)
    );
    """

    create_members_table = """
    CREATE TABLE IF NOT EXISTS members (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        role VARCHAR(255) NOT NULL,
        position VARCHAR(255) NOT NULL,
        faculty VARCHAR(255),
        resolution_id INT NOT NULL,
        FOREIGN KEY (resolution_id) REFERENCES resolutions(id)
    );
    """

    create_files_table = """
    CREATE TABLE IF NOT EXISTS files (
        id INT AUTO_INCREMENT PRIMARY KEY,
        file_name VARCHAR(255) NOT NULL,
        file_size INT NOT NULL,
        upload_date DATE NOT NULL,
        meeting_id INT NOT NULL,
        FOREIGN KEY (meeting_id) REFERENCES meetings(id)
    );
    """

    # Futtatás
    try:
        cursor.execute(create_meetings_table)
        cursor.execute(create_resolutions_table)
        cursor.execute(create_members_table)
        cursor.execute(create_files_table)
        print("A táblák sikeresen létrejöttek.")
    except Exception as e:
        print(f"Hiba a táblák létrehozásakor: {e}")
def delete_meeting(connection, meeting_id):
    cursor = connection.cursor()
    delete_query = "DELETE FROM meetings WHERE id = %s"
    cursor.execute(delete_query, (meeting_id,))
    connection.commit()
    print(f"Successfully deleted meeting with ID: {meeting_id}")

# Main execution
# connection = create_connection()
# if connection:
#     #create_table(connection)
#     #create_tables(connection)
#     delete_meeting(connection,1)
