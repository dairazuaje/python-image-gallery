from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from . import db
from . import secrets

app = Flask(__name__)


@app.route("/admin")
def admin():
    users = select_all()
    close()
    return render_template("admin.html", users=users)


@app.route("/admin/edit_user_form<fn>")
def edit_user(fn):
    user = fn
    return render_template("edit_user_form.html", user=user)


@app.route("/admin/process_edit_user_form<user>", methods=["POST"])
def process_edit_user_form(user):
    # username = request.form['username']
    password = request.form['password']
    fullname = request.form["fullname"]
    edit(user, password, fullname)
    return render_template("process_edit_user_form.html", user=user)


@app.route("/admin/add_user_form")
def add_user_form():
    return render_template("add_user_form.html")


@app.route("/admin/process_user_add_form", methods=["POST"])
def process_add_user_form():
    username = request.form['username']
    password = request.form['password']
    fullname = request.form["fullname"]
    add(username, password, fullname)
    return render_template("process_add_user_form.html", user=username)


@app.route("/admin/process_delete_user_form<user>", methods=["POST"])
def process_delete_user_form(user):
    delete(user)
    return render_template("process_delete_user_form.html", user=user)
