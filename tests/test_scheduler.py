# tests/test_scheduler.py
import pytest
import sqlite3
import os
from scheduler.scheduler import MockScheduler

TEST_DB = "test_campaign.db"

@pytest.fixture
def scheduler():
    """Fixture to set up and tear down the test database."""
    # Setup: create a scheduler instance with a test DB
    scheduler = MockScheduler(db_file=TEST_DB)
    scheduler.connect()
    scheduler.initialize_db()
    
    # Yield the scheduler instance to the test
    yield scheduler
    
    # Teardown: close connection and remove the test DB file
    scheduler.close()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_initialize_db(scheduler):
    """Test if the database and table are created correctly."""
    assert os.path.exists(TEST_DB)
    
    # Check if the table exists
    cursor = scheduler.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scheduled_posts';")
    table = cursor.fetchone()
    assert table is not None
    assert table['name'] == 'scheduled_posts'

def test_schedule_and_get_posts(scheduler):
    """Test scheduling a post and retrieving it."""
    # Initially, there should be no posts
    assert scheduler.get_all_scheduled_posts() == []

    # Schedule a post
    platform = "Twitter"
    content = "This is a test tweet!"
    date = "2025-10-26"
    scheduler.schedule_post(platform, content, date)

    # Retrieve posts and check
    posts = scheduler.get_all_scheduled_posts()
    assert len(posts) == 1
    post = posts[0]
    assert post['platform'] == platform
    assert post['content'] == content
    assert post['scheduled_date'] == date
    assert post['status'] == 'scheduled'

def test_schedule_multiple_posts(scheduler):
    """Test scheduling and retrieving multiple posts, checking order."""
    scheduler.schedule_post("LinkedIn", "Post 2", "2025-10-28")
    scheduler.schedule_post("Twitter", "Post 1", "2025-10-27")
    
    posts = scheduler.get_all_scheduled_posts()
    assert len(posts) == 2
    
    # Posts should be ordered by scheduled_date ASC
    assert posts[0]['content'] == "Post 1"
    assert posts[1]['content'] == "Post 2"

def test_invalid_date_format_scheduling(scheduler, caplog):
    """Test that scheduling with an invalid date format is handled."""
    scheduler.schedule_post("Twitter", "Invalid date post", "26-10-2025")
    
    # Check that an error was logged
    assert "Invalid date format for scheduling" in caplog.text
    
    # Ensure the post was not added to the DB
    posts = scheduler.get_all_scheduled_posts()
    assert len(posts) == 0
