"""
poop
"""
from flask import Blueprint, request, jsonify
from clank import base_model


main_bp = Blueprint("main", __name__)


@main_bp.route("/query", methods=["POST"])
def process_query():
    """
    poop
    """
    data = request.json
    query = data.get("query")
    # task = data.get("task", "general")

    response = base_model.generate_response(query)

    # if task == "sentiment":
    #     response = sentiment_model.analyze(query)
    # elif task == "summarization":
    #     response = summarization_model.summarize(query)
    # else:
    #     response = {"error": "Task not recognized"}

    return jsonify(response)

def register_routes(app):
    """
    poop
    """
    app.register_blueprint(main_bp)
