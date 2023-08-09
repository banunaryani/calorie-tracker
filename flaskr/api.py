from flask import (
    Blueprint,
    g,
    request,
    make_response,
    session,
    url_for,
    jsonify,
)

from flaskr.db import get_db
from flaskr.food import *

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/food", methods=["GET"])
def get_foods():
    keyword = request.args.get("q")
    cols = ["id", "user_id", "food_name", "food_calorie"]
    data = []
    foods = []

    if keyword is None:
        foods = get_all_foods()
    else:
        foods = get_foods_by_keyword(keyword, 5)

    for food in foods:
        data.append(dict(zip(cols, food)))

    return jsonify(data)
