from flask import Blueprint, request, abort, make_response, Response
# from .route_utilities import validate_model
from app.models.board import Board
from app.models.card import Card
from ..db import db

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

# GET ALL BOARDS FROM DB
@bp.get("")
def get_all_boards():
    query = db.select(Board)
    boards = db.session.scalars(query)
    boards_response = [board.to_dict() for board in boards]
    return boards_response


# @bp.get("/<goal_id>")
# def get_one_goal(goal_id):
#     goal = validate_model(Goal, goal_id)
#     return {"goal": goal.to_dict()}


# @bp.put("/<goal_id>")
# def update_goal(goal_id):
#     goal = validate_model(Goal, goal_id)
#     request_body = request.get_json()
#     goal.title = request_body["title"]

#     db.session.add(goal)
#     db.session.commit()

#     return {"goal": goal.to_dict()}


# @bp.post("")
# def create_goal():
#     request_body = request.get_json()

#     try:
#         new_goal = Goal.from_dict(request_body)

#     except KeyError as error:
#         response = {"details": f"Invalid data"}
#         abort(make_response(response, 400))

#     db.session.add(new_goal)
#     db.session.commit()

#     return {"goal": new_goal.to_dict()}, 201


# @bp.delete("/<goal_id>")
# def delete_goal(goal_id):
#     goal = validate_model(Goal, goal_id)
#     db.session.delete(goal)
#     db.session.commit()

#     message = f"Goal {goal_id} \"{goal.title}\" successfully deleted"
#     return {"details": message}


# @bp.get("/<goal_id>/tasks")
# def get_tasks_from_goal(goal_id):
#     goal = validate_model(Goal, goal_id)
#     tasks = [task.to_dict() for task in goal.tasks]
    
#     response = goal.to_dict()
#     response["tasks"] = tasks
#     return response


# @bp.post("/<goal_id>/tasks")
# def add_tasks_tp_goal(goal_id):
#     goal = validate_model(Goal, goal_id)
#     request_body = request.get_json()
#     task_ids = request_body["task_ids"]

#     for task_id in task_ids:
#         task = validate_model(Task, task_id)
#         goal.tasks.append(task)

#     db.session.commit()

#     response = {
#         "id": goal.id,
#         "task_ids": task_ids,
#     }
#     return response