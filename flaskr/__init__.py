import os

from flask import Flask

from flask import (
    redirect,
    url_for,
    g,
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/")
    def hello():
        if g.user is None:
            return redirect(url_for("auth.login"))

        return redirect(url_for("tracker.index"))

    from . import db

    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import food

    app.register_blueprint(food.bp)
    app.add_url_rule("/", endpoint="index")

    from . import tracker

    app.register_blueprint(tracker.bp)

    from . import api

    app.register_blueprint(api.bp)

    return app
