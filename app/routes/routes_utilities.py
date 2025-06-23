from flask import abort, make_response
from app.db import db

def validate_model_by_id(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response_message = {"message": f"{cls.__name__} id <{model_id}> is invalid."}
        abort(make_response(response_message, 400))       
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response_message = {"message": f"{cls.__name__} with id <{model_id}> is not found."}
        abort(make_response(response_message, 404))

    return model

def create_model_inst_from_dict_with_response(cls, inst_data):
    try:
        new_instance = cls.from_dict(inst_data)
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_instance)
    db.session.commit()
    response = {f"{cls.__name__.lower()}": new_instance.to_dict()}
    return response, 201
    