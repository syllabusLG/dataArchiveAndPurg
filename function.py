import cx_Oracle
from datetime import datetime

#Database connection info

HOST_NAME = "REG_DB_HOST"
SERVICE_NAME = "REG_DB_SN"
PORT = "REG_DB_PORT"
USERNAME = "REG_DB_USER"
PASSWORD = "REG_DB_PASS"

#Coonect to the DB
def get_connection():
    con = cx_Oracle.makedsn(HOST_NAME, PORT, service_name=SERVICE_NAME)
    return cx_Oracle.connect(USERNAME, PASSWORD, con)

# Function to create an archive table if it doesn't exist
def create_archive_table(cursor, table_name):
    archive_table_name = f"{table_name}_HIST"
    # Check if the archive table already exists
    cursor.execute(f"""
        SELECT COUNT(*) 
        FROM all_tables 
        WHERE table_name = UPPER('{archive_table_name}')
    """)
    if cursor.fetchone()[0] == 0:
        # Create the archive table with the same structure as the original
        cursor.execute(f"""
            CREATE TABLE {archive_table_name} AS 
            SELECT * FROM {table_name} WHERE 1=0
        """)
        print(f"Archive table '{archive_table_name}' created.")
    else:
        print(f"Archive table '{archive_table_name}' already exists.")

# Function to archive data from a table and purge table
def archive_table_data(cursor, table_name, condition):
    archive_table_name = f"{table_name}_HIST"
    # Insert data into the archive table
    cursor.execute(f"""
        INSERT INTO {archive_table_name}
        SELECT * FROM {table_name} WHERE {condition}
    """)
    print(f"Data archived to table '{archive_table_name}'.")

    # Delete the archived data from the original table
    cursor.execute(f"""
        DELETE FROM {table_name} WHERE {condition}
    """)
    print(f"Archived data deleted from table '{table_name}'.")

# Main function to archive tables in the schema
def archive_schema_tables(condition):
    try:
        # Connect to the database
        conn = get_connection()
        cursor = conn.cursor()
        # Fetch all tables in the schema
        cursor.execute("""
            SELECT table_name 
            FROM user_tables
        """)
        tables = [row[0] for row in cursor.fetchall()]
        for table_name in tables:
            print(f"\nProcessing table: {table_name}")
            create_archive_table(cursor, table_name)  # Ensure archive table exists
            archive_table_data(cursor, table_name, condition)  # Archive data
        # Commit the changes
        conn.commit()
        print("\nArchiving process completed successfully.")
    except cx_Oracle.Error as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the database connection
        if conn:
            conn.close()

