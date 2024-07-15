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


# change_column_type()