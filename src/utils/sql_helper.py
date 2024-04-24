import psycopg2.extensions as ext

def get_or_create_id(cur: ext.cursor, conn: ext.connection, table_name: str, column_name: str, value: str) -> str:
    """Get the id for a value in a table, and create a new one if it doesn't exist.

    Args:
        cur (ext.cursor): The cursor object tfrom psycopg2 to execute queries.
        conn (ext.connection): The connection object from psycopg2 to commit changes.
        table_name (str): The name of the table to query.
        column_name (str): The name of the column to query.
        value (str): The value to query for.

    Returns:
        str: The id of the value in the table.
    """
    cur.execute(f"SELECT id FROM {table_name} WHERE {column_name} = %s", (value,)) # make sure to always use string interpolation to avoid SQL injection
    result: tuple[str, ...] = cur.fetchone()
    if result:
        id = result[0]
    else:
        cur.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (%s) RETURNING id", (value,))
        conn.commit()
        id = cur.fetchone()[0]
    return id

