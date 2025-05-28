import sqlite3
import unittest

class TestDBSchema(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect("project.db")
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_create_tables(self):
        self.cur.executescript("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        );
        """)
        # Check tables exist
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in self.cur.fetchall()]
        self.assertIn("authors", tables)
        self.assertIn("magazines", tables)
        self.assertIn("articles", tables)

if __name__ == '__main__':
    unittest.main()
