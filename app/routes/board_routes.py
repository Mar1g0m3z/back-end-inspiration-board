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

# POST ONE BOARD, RETURN {"GOAL": {GOAL DICTIONARY}}
@bp.post("")
def create_board():
    request_body = request.get_json()
    return create_model_inst_from_dict_with_response(Board, request_body)

# GET BOARD BY ID
@bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_model_by_id(Board, board_id)
    return nested_dict(Board, board)

# GET CARDS FOR ONE BOARD, RETURN BOARD DICTIONARY WITH CARDS LIST
@bp.get("/<board_id>/cards")
def get_cards_of_one_board(board_id):
    board = validate_model_by_id(Board, board_id)
    return board.to_dict()