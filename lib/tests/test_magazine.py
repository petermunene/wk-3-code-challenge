import os
import sqlite3
import unittest
from lib.models.magazine import Magazine
from lib.models.author import Author  # needed for contributors test

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

class TestMagazine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def setUp(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

        # Insert dummy author for foreign key relations
        self.cur.execute("INSERT INTO authors (name) VALUES (?)", ("Author1",))
        self.conn.commit()
        self.author_id = self.cur.lastrowid

    def tearDown(self):
        self.conn.close()

    def test_save_and_find_magazine(self):
        mag = Magazine(name="Fashion Weekly", category="Fashion & Lifestyle")
        mag.save()  # uses project.db internally
        self.assertIsNotNone(mag.id)

        found = Magazine.find_by_id(mag.id)
        self.assertEqual(found.name, "Fashion Weekly")

        found_by_name = Magazine.find_by_name("Fashion Weekly")
        self.assertEqual(found_by_name.category, "Fashion & Lifestyle")

    def test_articles_and_contributors(self):
        mag = Magazine(name="Tech Today", category="Technology & Gadgets")
        mag.save()

        # Insert article linked to dummy author and this magazine
        self.cur.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
            ("Article1", self.author_id, mag.id)
        )
        self.conn.commit()

        articles = mag.articles()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Article1")

        contributors = mag.contributors()
        self.assertEqual(len(contributors), 1)
        self.assertEqual(contributors[0].id, self.author_id)

if __name__ == "__main__":
    unittest.main()