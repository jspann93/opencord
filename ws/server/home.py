from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from .db import get_db
from flask import session
# Possibly get flast_login 

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    print(len(session))
    s = None
    if len(session) > 0: 
        s = 1

    db = get_db()


    return render_template("home/home.html", current_user=s)