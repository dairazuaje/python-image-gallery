import os
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from functools import wraps
from ..data.db import  *
from ..aws.s3 import *

from werkzeug.utils import secure_filename

BUCKET_NAME = "edu.au.cc.image-gallery-photos-dza0042"
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['BUCKET_NAME'] = BUCKET_NAME
app.secret_key = get_secret_flask_session()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            directory_name = str(session["username"]) + "/" + filename
            put_object(BUCKET_NAME, directory_name, file)
            add_image_db(session["username"], filename)
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            return redirect("/")
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            return redirect("/login")
        return view(**kwargs)
    return decorated


def requires_user(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_user():
            return redirect("/login")
        return view(**kwargs)
    return decorated


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/debug_session")
def debug_session():
    result = ""
    for key,value in session.items():
        result += key + "->" + str(value) +  "<br>"
    return result


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/process_login", methods=["POST"])
def process_login():
    username = request.form["username"]
    password = request.form["password"]
    if check_password(username, password):
        session["username"] = request.form["username"]
        return redirect("/debug_session")
    return redirect("/invalid_login")


@app.route("/invalid_login")
def invalid_login():
    return "Invalid"


def check_admin():
    return 'username' in session and session["username"] == "dza0042"


@app.route("/admin")
@requires_admin
def admin():
    users = select_all()
    close()
    return render_template("admin.html", users=users)


@app.route("/admin/edit_user_form<fn>")
@requires_admin
def edit_user(fn):

    user = fn
    return render_template("edit_user_form.html", user=user)


@app.route("/admin/process_edit_user_form<user>", methods=["POST"])
@requires_admin
def process_edit_user_form(user):
    # username = request.form['username']
    password = request.form['password']
    fullname = request.form["fullname"]
    edit(user, password, fullname)
    return render_template("process_edit_user_form.html", user=user)


@app.route("/admin/add_user_form")
@requires_admin
def add_user_form():
    return render_template("add_user_form.html")


@app.route("/admin/process_user_add_form", methods=["POST"])
@requires_admin
def process_add_user_form():
    username = request.form['username']
    password = request.form['password']
    fullname = request.form["fullname"]
    if request.form["type"]:
        print("User will be admin")
    else:
        print("User will not be admin")
    add(username, password, fullname)
    return render_template("process_add_user_form.html", user=username)


@app.route("/admin/process_delete_user_form<user>", methods=["POST"])
@requires_admin
def process_delete_user_form(user):
    delete(user)
    return render_template("process_delete_user_form.html", user=user)
