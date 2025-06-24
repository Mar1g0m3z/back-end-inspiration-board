from flask import Blueprint, request, Response, make_response
from app.models.card import Card
from app.models.board import Board
from app.db import db
from .routes_utilities import validate_model_by_id, create_model_inst_from_dict_with_response, nested_dict
from sqlalchemy import delete

bp = Blueprint("cards_bp", __name__, url_prefix = "/cards")


# ===========================================
# This route should be moved to board_routes
# -------------------------------------------
# Endpoint: POST /boards/<board_id>/cards
# Purpose: Create a card under a specific board
# # TODO: Move to boards blueprint and include board_id association logic
# ===========================================
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

    return new_card.to_dict(), 200
    # return create_model_inst_from_dict_with_response(Card, request_body)


#################### End point?
# Choose between 
    # /cards/<card_id>/like
    # /boards/<board_id>/cards/<card_id>/like
# Increment the likes_count of a card by 1
@bp.patch("/<card_id>/like")
def increment_card_likes(card_id):
    card = validate_model_by_id(Card, card_id)
    card.likes_count += 1
    db.session.commit()

    return card.to_dict(), 200

#################### End point?
# choose between 
    # "/boards/<board_id>/cards/<card_id>”
    #  "/cards/<card_id>""
@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model_by_id(Card, card_id)

    db.session.delete(card)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")


#################### End point?
    # Delete all boards and card
    # "/boards/delete_all”
@bp.delete("/delete_all")
def delete_all_boards_and_cards():
    # Delete all cards
    db.session.execute(delete(Card))
    # Delete all boards
    db.session.execute(delete(Board))
    db.session.commit()

    return Response(status=204, mimetype="application/json")
