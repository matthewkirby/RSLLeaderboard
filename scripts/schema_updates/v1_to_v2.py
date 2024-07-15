import sqlite3
import settings

def create_connection(db_path):
    """ Create database connection and execute any queries that should be run every time. """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def change_column_type():
    # In the racelist table, change the column type from INT to TEXT
    conn = create_connection(settings.racelist_db_path)
    cursor = conn.cursor()

    try:
        conn.execute("PRAGMA foreign_keys = OFF;")
        # Make the new table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS new_racelist (
                slug TEXT PRIMARY KEY,
                url TEXT,
                ended_at DATETIME,
                season TEXT
            );
        ''')

        # Copy data from old table to new table
        cursor.execute('''
            INSERT INTO new_racelist (slug, url, ended_at, season)
            SELECT slug, url, ended_at, CAST(season AS TEXT)
            FROM racelist;
        ''')

        # Swap over the new table for the old table
        cursor.execute('DROP TABLE racelist;')
        cursor.execute('ALTER TABLE new_racelist RENAME TO racelist;')
        conn.execute("PRAGMA foreign_keys = ON;")

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def add_column(table_name, column_name, column_type, column_default):
    conn = create_connection(settings.racelist_db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        if column_name not in column_names:
            print("Adding column:", column_name)
            cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} DEFAULT {column_default};')
        else:
            print(f"{column_name} already exists.")
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()



change_column_type()
add_column("entrants", "include", "BOOLEAN", 1)
add_column("entrants", "ruleset", "TEXT", "Standard")