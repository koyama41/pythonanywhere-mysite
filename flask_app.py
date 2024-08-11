# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from configparser import ConfigParser

app = Flask(__name__)

auth = HTTPBasicAuth()
@auth.get_password
def get_pw(username):
    config = ConfigParser()
    config.read("/home/koyama41/mysite.ini")
    if "user.password" in config.sections():
        users = config["user.password"]
        if username in users:
            return users.get(username)
    return None

@app.route("/")
@auth.login_required
def hello_world():
    return "<HTML><HEAD><TITLE>top</TITLE></HEAD><BODY><P>welcome!</P></BODY></HTML>"

database = {}

@app.route("/dbtest/<name>", methods=["GET", "DELETE", "POST", "PUT"])
@auth.login_required
def dbtest(name):
    if request.method == "GET":
        if name not in database:
            return {"error": f"unknown user: {name}"}, 404
        return database[name], 200

    if request.method == "DELETE":
        if name not in database:
            return {"error": f"unknown user: {name}"}, 404
        del database[name]
        return {"message": f"{name} is deleted"}, 204

    newData = name not in database
    if not newData:
        if request.method == "POST":
            return {"error": f"{name} already exists"}, 409
    database[name] = request.json
    if newData:
        return {"message": f"{name} is created"}, 201
    else:
        return {"message": f"{name} is overwritten"}, 204
