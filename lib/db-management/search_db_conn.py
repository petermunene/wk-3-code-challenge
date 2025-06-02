def get_connection():
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()