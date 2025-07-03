import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.board import Board
from app.models.card import Card

load_dotenv()

@pytest.fixture
def app():
    # create the app with a test configuration
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# This fixture gets called in every test that
# references "one_board"
# This fixture creates a task and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(title="Learn how to cook", 
                    owner="Michael")
    db.session.add(new_board)
    db.session.commit()


# This fixture gets called in every test that
# references "three_boards"
# This fixture creates three tasks and saves
# them in the database
@pytest.fixture
def three_boards(app):
    db.session.add_all([
        Board(title="Find new hobbies", 
            owner="Anna"),
        Board(title="Become more social", 
            owner="Fedor"),
        Board(title="Find a dream job", 
            owner="Sasha")
    ])
    db.session.commit()