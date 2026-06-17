import os
import sqlite3

DATEBASE_NAME = "dorm.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_connection():
    db_path = os.path.join(BASE_DIR, DATEBASE_NAME)
    return sqlite3.connect(db_path)


# Run sql script unser db/scripts/
def run_sql(filename):
    filepath = os.path.join(BASE_DIR, "scripts", filename)
    conn = get_connection()
    with open(filepath, "r") as f:
        conn.executescript(f.read())
    conn.close()


# if __name__ == "__main__":
#     run_sql("001_create_db.sql")
#     run_sql("002_add_test_user.sql")
