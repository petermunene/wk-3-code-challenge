import os
import sqlite3
import unittest
from lib.models.article import Article

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

class TestArticle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def setUp(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

        # Insert dummy author and magazine for FK relations
        self.cur.execute("INSERT INTO authors (name) VALUES (?)", ("Author1",))
        self.author_id = self.cur.lastrowid

        self.cur.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Mag", "Technology & Gadgets"))
        self.magazine_id = self.cur.lastrowid

        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_save_and_find_article(self):
        article = Article(title="Test Article", author_id=self.author_id, magazine_id=self.magazine_id)
        article.save()  # uses project.db internally
        self.assertIsNotNone(article.id)

        found = Article.find_by_id(article.id)
        self.assertEqual(found.title, "Test Article")

    def test_find_by_author_and_magazine(self):
        article = Article(title="Another Article", author_id=self.author_id, magazine_id=self.magazine_id)
        article.save()

        articles_by_author = Article.find_by_author(self.author_id)
        self.assertTrue(any(a.id == article.id for a in articles_by_author))

        articles_by_magazine = Article.find_by_magazine(self.magazine_id)
        self.assertTrue(any(a.id == article.id for a in articles_by_magazine))

if __name__ == "__main__":
    unittest.main()
