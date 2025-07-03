from flask import Blueprint, request, abort, make_response, Response
from .routes_utilities import validate_model_by_id, create_model_inst_from_dict_with_response, nested_dict
from app.models.board import Board
from app.models.card import Card
from ..db import db

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

# GET ALL BOARDS FROM DB
@bp.get("")
def boards():
    boards = db.session.scalars(db.select(Board).order_by(Board.title))
    return [board.to_dict() for board in boards]

# POST ONE BOARD, RETURN {"BOARD": {BOARD DICTIONARY}}
@bp.post("")
def create_board():
    request_body = request.get_json()
    return create_model_inst_from_dict_with_response(Board, request_body)

# GET CARDS FOR ONE BOARD, RETURN BOARD DICTIONARY WITH CARDS LIST
@bp.get("/<board_id>/cards")
def get_cards_of_one_board(board_id):
    board = validate_model_by_id(Board, board_id)
    return board.to_dict()

# CREATE CARDS FOR ONE BOARD, RETURN THE NEW CARD
@bp.post("/<board_id>/cards")
def create_card(board_id):
    board = validate_model_by_id(Board, board_id)

    # create Card model
    request_body = request.get_json()
    request_body["board_id"] = board_id

    try:
        new_card = Card.from_dict(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    board.cards.append(new_card)
    db.session.add(new_card)
    db.session.commit()

    return new_card.to_dict(), 201

