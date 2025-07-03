from app.models.board import Board
from app.db import db
import pytest

def test_get_all_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Learn how to cook",
            "owner": "Michael",
            "cards": []
        }
    ]

def test_get_all_boards_three_saved_boards(client, three_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3

    expected_boards = [
        {"title": "Find new hobbies", "owner": "Anna"},
        {"title": "Become more social", "owner": "Fedor"},
        {"title": "Find a dream job", "owner": "Sasha"}
    ]

    for board in expected_boards:
        assert any(
            returned["title"] == board["title"]
            and returned["owner"] == board["owner"]
            and returned["cards"] == []
            for returned in response_body
        )