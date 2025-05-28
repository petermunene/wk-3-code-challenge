import os
import sqlite3
import unittest
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

SCHEMA_FILE = "lib/db-management/schema.sql"
DB_FILE = "project.db"

def initialize_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    with open(SCHEMA_FILE, "r") as f:
        schema_sql = f.read()
        conn.executescript(schema_sql)
    conn.commit()
    conn.close()

class TestAuthor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Run once before all tests
        initialize_database()

    def setUp(self):
        # Before each test, open a connection and add dummy magazine
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

        # Insert dummy magazine
        self.cur.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Mag", "Technology & Gadgets"))
        self.conn.commit()
        self.magazine_id = self.cur.lastrowid

    def tearDown(self):
        self.conn.close()

    def test_save_and_find_author(self):
        author = Author(name="Alice")
        author.save()  # Uses project.db internally, no conn passed
        self.assertIsNotNone(author.id)

        # Retrieve author directly from DB to check
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT name FROM authors WHERE id=?", (author.id,))
        row = cur.fetchone()
        conn.close()
        self.assertEqual(row[0], "Alice")

    def test_articles_and_magazines(self):
        author = Author(name="Bob")
        author.save()

        # Create a dummy magazine object matching inserted magazine
        dummy_magazine = Magazine(id=self.magazine_id, name="Tech Mag", category="Technology & Gadgets")

        # Add article for author
        article = author.add_article(magazine=dummy_magazine, title="Cool Tech")
        self.assertEqual(article.title, "Cool Tech")

        # Fetch author's articles using Author method
        articles = author.articles()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Cool Tech")

        # Fetch magazines using Author method
        mags = author.magazines()
        self.assertEqual(len(mags), 1)
        self.assertEqual(mags[0].name, "Tech Mag")

if __name__ == "__main__":
    unittest.main()