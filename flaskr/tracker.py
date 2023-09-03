import functools
import datetime
from pprint import pprint

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.exceptions import abort

from flaskr.db import get_db
from flaskr.auth import login_required

bp = Blueprint("tracker", __name__, url_prefix="/tracker")


@bp.route("", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        food_id = request.form["food_id"]
        quantity = request.form["quantity"]

        db = get_db()
        error = None

        if not food_id:
            error = "Food field is required"
        elif not quantity:
            error = "Food quantity field is required"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO tracker (tracking_date,user_id,food_id,quantity)"
                    " VALUES (?, ?, ?, ?)",
                    (
                        datetime.date.today().strftime("%Y-%m-%d"),
                        g.user["id"],
                        food_id,
                        quantity,
                    ),
                )
                db.commit()
            except db.Error as e:
                error = str(e)
            else:
                return redirect(url_for("tracker.index"))

        flash(error)

    return render_template(
        "tracker/index.html",
        today=get_today_tracking(True),
        date=datetime.date.today().strftime("%d-%m-%Y"),
        foods=get_foods(check_user=True),
        total_calorie=get_sum_today_tracking(),
    )


def get_today_tracking(check_user):
    tracking = (
        get_db()
        .execute(
            "SELECT *, quantity*f.food_calorie/100 AS calorie"
            " FROM tracker t JOIN food f ON t.food_id=f.id"
            " WHERE tracking_date = CURRENT_DATE"
        )
        .fetchall()
    )

    if check_user is False:
        abort(403)

    return tracking


def get_sum_today_tracking():
    sum = (
        get_db()
        .execute(
            "SELECT SUM(quantity*f.food_calorie/100) AS total_calorie"
            " FROM tracker t JOIN food f ON t.food_id=f.id"
            " WHERE tracking_date = CURRENT_DATE"
        )
        .fetchone()
    )

    return sum


def get_foods(check_user):
    foods = (
        get_db()
        .execute(
            "SELECT f.id, food_name, food_calorie, user_id, username"
            " FROM food f JOIN user u ON f.user_id=u.id"
        )
        .fetchall()
    )

    if check_user is False:
        abort(403)

    return foods


def get_tracking(id, check_user=True):
    tracking = (
        get_db()
        .execute(
            "SELECT t.id, t.tracking_date, t.food_id, t.quantity, user_id, username"
            " FROM tracker t JOIN user u ON t.user_id=u.id"
            " WHERE t.id = ?",
            (id,),
        )
        .fetchone()
    )

    if not check_user:
        abort(403)

    return tracking


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        tracking_date = request.form["tracking_date"]
        food_id = request.form["food_id"]
        quantity = request.form["quantity"]

        db = get_db()
        error = None

        if not tracking_date:
            error = "Date field is required"
        elif not food_id:
            error = "Food field is required"
        elif not quantity:
            error = "Food quantity field is required"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO tracker (tracking_date,user_id,food_id,quantity)"
                    " VALUES (?, ?, ?, ?)",
                    (
                        datetime.date.today().strftime("%Y-%m-%d"),
                        g.user["id"],
                        food_id,
                        quantity,
                    ),
                )
                db.commit()
            except db.Error as e:
                error = str(e)
            else:
                return redirect(url_for("tracker.index"))

        flash(error)

    return render_template(
        "tracker/create.html",
        foods=get_foods(check_user=True),
        date=datetime.date.today(),
    )


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    item = get_tracking(id, True)
    foods = get_foods(True)

    if request.method == "POST":
        tracking_date = request.form["tracking_date"]
        food_id = request.form["food_id"]
        quantity = request.form["quantity"]

        db = get_db()
        error = None

        if not quantity:
            error = "Quantity is required"

        if error is not None:
            flash(error)
        else:
            db.execute(
                "UPDATE tracker SET tracking_date = ?, food_id = ?, quantity = ? WHERE id = ?",
                (tracking_date, food_id, quantity, id),
            )
            db.commit()
            return redirect(url_for("tracker.index"))

    return render_template(
        "tracker/update.html", tracking=item, date=datetime.date.today(), foods=foods
    )


@bp.route("/<int:id>/delete", methods=("POST", "GET"))
@login_required
def delete(id):
    get_tracking(id)
    db = get_db()
    db.execute("DELETE FROM tracker WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("tracker.index"))
