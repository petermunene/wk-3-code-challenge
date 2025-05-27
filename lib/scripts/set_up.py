
def setup_database():
    conn = sqlite3.connect("project.db")
    cursor = conn.cursor()

    with open("lib/db-management/schema.sql", "r") as f:
        schema = f.read()
        cursor.executescript(schema)

    conn.commit()
    conn.close()
    print("Database setup complete.")

    

if __name__ == "__main__":
    setup_database()