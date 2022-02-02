from flask import (
    Flask,
    request as req,
    g,
    redirect,
    render_template,
    session,
    url_for
)

from json import loads, dumps

from mylib import *

def read(filename: str):
    f = open(filename, "r")
    o = f.read()
    f.close()
    return o

app = Flask(__name__)
app.secret_key = "very secreT K1 p3@se d0n7 5hre"

db = LoginDataBase()
db.add(User(
    username="mowitek",
    password="jeff",
    email="test@aaa.de",
    name="franz xafer",
    user_permissions=2
))

db.add(User(
    username="user",
    password="jeff",
    email="none",
    name="franz xafer 2",
    user_permissions=1
))

db.add(User(
    username="admin",
    password="jeff",
    email="aaaa",
    name="aaaaa",
    user_permissions=3
))

k = Kalender()
# k.set(Date(year=2022, month=0, day=20), "16:00-16:05", ["ROOT"])

def get_login() -> User:
    if (c := session.get("cookie")):
        if (c := Cookie.loads(c)):
            if (c.user["username"] in db):
                return db[c.user["username"]]

def get_permission_level() -> bool:
    u = get_login()
    if u:
        return u.info["user_permissions"]
    return 0

def check_if_allowed(lvl: int) -> bool:
    return get_permission_level() >= lvl


# login managment
@app.route('/login', methods=['POST'])
def login_post():
    r: dict = loads(req.data)

    err = None

    user = r.get('username')
    password = r.get('password')

    if user in db and db.get(user).info.get("password") == password:
        user = db.get(user)
        session.pop("cookie", None)
        session["cookie"] = Cookie(user).saves()
    else:
        session["cookie"] = None
        err = 403

    return dumps({"error": err})

@app.route("/logout", methods=['POST'])
def logout_post():
    cookie = None

    err = None

    if session.get("cookie"):
        cookie = Cookie.loads(session["cookie"])

    if cookie:
        session.pop("cookie", None)
    else:
        err = 404


    return dumps({"error": err})


@app.route("/register", methods=["POST"])
def register_post():
    r: dict = loads(req.data)
    err = None
    try:
        u = User(
            username=r["username"],
            password=r["password"],
            email=r["email"],
            name=["name"],
            user_permissions=1
        )
    except:
        err = 400

    if u not in db:
        succes = db.add(u)
    else:
        err = 403

    return dumps({"error": err})


# api
# this gets error messages for eg display
@app.route("/api/error/get_msg", methods=["POST"])
def api_error_get_msg():
    return dumps(Error()(loads(req.data)))

# this is for reserving the appointment
@app.route("/api/appointment/add", methods=["POST"])
def api_appointment_add():
    r: dict = loads(req.data)
    err = None
    u = get_login()

    try:
        d = Date(
            year=r.get("year"),
            month=r.get("month"),
            day=r.get("day")
        )
    except:
        err = 400

    if u:
        rs = k.set(d, r.get("time"), u)

    else:
        err = 401
        rs = False

    return dumps({"error": err})

# this allows you to cancel your appointment
@app.route("/api/appointment/del", methods=["POST"])
def api_appointment_del():
    r: dict = loads(req.data)
    err = None
    u = get_login()

    try:
        d = Date(
            year=r.get("year"),
            month=r.get("month"),
            day=r.get("day")
        )
    except:
        err = 400

    t = r.get("time")
    T = k.get(d, t)
    if T:
        if u.info["username"] == T["username"]:
            k.rem(d, t)
        else:
            err = 403
    else:
        err = 404

    return dumps({"error": err})

# get taken dates
@app.route("/api/get_dates_censored", methods=["POST"])
def api_get_dates_censored():
    r: dict = loads(req.data)
    err = None

    try:
        rs = k.dump(Date(year = r["year"], month=r["month"]))

        # censoring + stipping
        rs_f = {}
        for d in rs:
            rs_f[d] = []
            for t in rs[d]:
                rs_f[d].append(t)

    except:
        err = 400
        rs = None

    return dumps({"data": rs_f, "error": err})

# get a list of dates
@app.route("/api/get_dates", methods=["POST"])
def api_get_dates():
    r: dict = loads(req.data)
    err = None
    rs = {}

    if not check_if_allowed(2):
        err = 403

    else:
        try:
            rs = k.dump(Date(year = r["year"], month=r["month"]))

            # stripping the user class
            rs_index = {}
            rs_map = {}
            for d in rs:
                rs_map[d] = {}
                for t in rs[d]:
                    rs_map[d][t] = {}
                    if rs[d][t]["username"] not in rs_index:
                        rs_index[rs[d][t]["username"]] = rs[d][t].jsonify()
                    rs_map[d][t] = rs[d][t]["username"]

        except:
            err = 400

    return dumps({"map": rs_map, "indexes": rs_index, "error": err})

# get own appointments
@app.route("/api/user/me", methods=["POST"])
def api_user_me():
    r: dict = loads(req.data)
    u = get_login()
    data = {}
    err = None

    if u:
        data["appointments"] = k.get_user_appointments(u)
        data["username"] = u.info["username"]
        data["name"] = u.info["name"]
        data["email"] = u.info["email"]

    return dumps({"error": None, "data": data})

@app.route("/api/user/get", methods=["POST"])
def api_user_get():
    r: dict = loads(req.data)
    u = get_login()
    data = {}
    err = None

    target = db.get(r.get("user"))
    if target:
        target = target.jsonify()


    return dumps(target)


# libs and stuff
@app.route("/public/user.js")
def public_get_userjs():
    return read("user.js")
@app.route("/public/util.js")
def public_get_utiljs():
    return read("util.js")



@app.route('/')
def home():
    return redirect("/kalender")

@app.route("/kalender")
def kalender():
    return read("kalender.html")

@app.route("/kalender_view")
def kalender_root():
    if not check_if_allowed(2): return Error()(403)

    return read("kalender_view.html")

import logging
logging.getLogger('werkzeug').setLevel(logging.ERROR)
app.run(port=80, host="0.0.0.0", debug=False)
