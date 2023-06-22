from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("food", __name__)


@bp.route("/food")
def index():
    db = get_db()
    food_list = db.execute(
        "SELECT f.id, f.user_id, f.nama, f.calorie_per_100gr"
        " FROM food f JOIN user u ON f.user_id=u.id"
        " ORDER BY nama"
    ).fetchall()

    return render_template("food/index.html", food_list=food_list)


@bp.route("/food/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        food_name = request.form["food_name"]
        calorie = request.form["calorie"]
        error = None

        if not food_name:
            error = "Food name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO food (nama, calorie_per_100gr, user_id)"
                " VALUES (?, ?, ?)",
                (
                    food_name,
                    calorie,
                    g.user["id"],
                ),
            )
            db.commit()
            return redirect(url_for("food.index"))

    return render_template("food/create.html")


def get_food(id, check_user=True):
    food = (
        get_db()
        .execute(
            "SELECT f.id, nama, calorie_per_100gr, user_id, username"
            " FROM food f JOIN user u ON f.user_id=u.id"
            " WHERE f.id = ?",
            (id,),
        )
        .fetchone()
    )

    if food is None:
        abort(404, f"Food id {id} doesn't exist.")

    if check_user and food["user_id"] != g.user["id"]:
        abort(403)

    return food


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    food = get_food(id)

    if request.method == "POST":
        food_name = request.form["food_name"]
        calorie = request.form["calorie"]
        error = None

        if not food_name:
            error = "Food name is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE food SET nama = ?, calorie_per_100gr = ?" " WHERE id = ?",
                (food_name, calorie, id),
            )
            db.commit()
            return redirect(url_for("food.index"))

    return render_template("food/update.html", food=food)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_food(id)
    db = get_db()
    db.execute("DELETE FROM food WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("food.index"))
