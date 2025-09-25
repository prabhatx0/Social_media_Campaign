# scheduler/scheduler.py
import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
DB_FILE = "campaign.db"

class MockScheduler:
    """
    A mock scheduler that uses SQLite to store and manage scheduled posts.
    """
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.row_factory = sqlite3.Row
            logging.info(f"Connected to database: {self.db_file}")
        except sqlite3.Error as e:
            logging.error(f"Database connection error: {e}")
            raise

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed.")

    def initialize_db(self):
        """Creates the scheduled_posts table if it doesn't exist."""
        if not self.conn:
            self.connect()
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS scheduled_posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        platform TEXT NOT NULL,
                        content TEXT NOT NULL,
                        scheduled_date TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'scheduled',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                logging.info("Database initialized successfully.")
        except sqlite3.Error as e:
            logging.error(f"Error initializing database: {e}")

    def schedule_post(self, platform: str, content: str, scheduled_date: str):
        """
        Saves a post to the database.

        Args:
            platform: The social media platform (e.g., "Twitter").
            content: The text of the post.
            scheduled_date: The date for the post in "YYYY-MM-DD" format.
        """
        if not self.conn:
            self.connect()
        try:
            # Validate date format
            datetime.strptime(scheduled_date, '%Y-%m-%d')
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO scheduled_posts (platform, content, scheduled_date) VALUES (?, ?, ?)",
                    (platform, content, scheduled_date)
                )
            logging.info(f"Scheduled post for {platform} on {scheduled_date}")
        except ValueError:
            logging.error(f"Invalid date format for scheduling: {scheduled_date}. Use YYYY-MM-DD.")
        except sqlite3.Error as e:
            logging.error(f"Error scheduling post: {e}")
            
    def get_all_scheduled_posts(self) -> list:
        """
        Retrieves all posts from the scheduled_posts table.

        Returns:
            A list of dictionaries representing the scheduled posts.
        """
        if not self.conn:
            self.connect()
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("SELECT id, platform, content, scheduled_date, status FROM scheduled_posts ORDER BY scheduled_date ASC")
                posts = [dict(row) for row in cursor.fetchall()]
                return posts
        except sqlite3.Error as e:
            logging.error(f"Error retrieving scheduled posts: {e}")
            return []
