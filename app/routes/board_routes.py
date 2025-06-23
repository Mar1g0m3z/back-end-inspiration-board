from flask import Blueprint, request, abort, make_response, Response
# from .route_utilities import validate_model
from app.models.board import Board
from app.models.card import Card
from ..db import db

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

# GET ALL BOARDS FROM DB
@bp.get("")
def boards():
    boards = db.session.scalars(db.select(Board).order_by(Board.title))
    return [board.to_dict() for board in boards]
