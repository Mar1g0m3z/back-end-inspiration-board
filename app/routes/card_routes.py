from flask import Blueprint, request, Response, make_response
from app.models.card import Card
from app.models.board import Board
from app.db import db
from .routes_utilities import validate_model_by_id, create_model_inst_from_dict_with_response, nested_dict
from sqlalchemy import delete

bp = Blueprint("cards_bp", __name__, url_prefix = "/cards")

# Increment the likes_count of a card by 1
@bp.patch("/<card_id>/like")
def increment_card_likes(card_id):
    card = validate_model_by_id(Card, card_id)
    card.likes_count += 1
    db.session.commit()

    return card.to_dict(), 200

# Delete a card
@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model_by_id(Card, card_id)

    db.session.delete(card)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")
