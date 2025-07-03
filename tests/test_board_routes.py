from app.models.board import Board
from app.models.card import Card

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

def test_create_board(client, app):
    # Arrange
    request_data = {
        "title": "My New Board",
        "owner": "Alex"
    }

    # Act
    response = client.post("/boards", json=request_data)
    response_body = response.get_json()

    # Assert: response
    assert response.status_code == 201
    assert "board" in response_body

    board = response_body["board"]
    assert board["title"] == request_data["title"]
    assert board["owner"] == request_data["owner"]
    assert board["cards"] == []
    assert "id" in board and isinstance(board["id"], int)

    # Assert: database
    query = db.select(Board).where(Board.id == board["id"])
    db_board = db.session.scalar(query)
    assert db_board is not None
    assert db_board.title == request_data["title"]
    assert db_board.owner == request_data["owner"]
    assert db_board.cards == []

def test_get_cards_for_board_no_cards(client, one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Learn how to cook",
        "owner": "Michael",
        "cards": []
    }

def test_get_cards_for_board_with_cards(client, one_board_with_cards):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == 1
    assert response_body["title"] == "Learn how to code"
    assert response_body["owner"] == "Sasha"
    assert len(response_body["cards"]) == 2
    messages = [card["message"] for card in response_body["cards"]]
    assert "Keep learning Python" in messages
    assert "Understand Linked lists" in messages

def test_create_card_for_existing_board(client, app, one_board):
    # Arrange
    request_data = {
        "message": "Buy some cooking books",
    }

    # Act
    response = client.post("/boards/1/cards", json=request_data)
    response_body = response.get_json()

    # Assert: response
    assert response.status_code == 201
    assert response_body["message"] == request_data["message"]
    assert response_body["likes_count"] == 0
    assert response_body["board_id"] == 1
    assert "id" in response_body

    # Assert: database
    query = db.select(Card).where(Card.id == response_body["id"])
    db_card = db.session.scalar(query)

    assert db_card is not None
    assert db_card.message == request_data["message"]
    assert db_card.likes_count == 0
    assert db_card.board_id == 1