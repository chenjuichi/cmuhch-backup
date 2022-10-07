import socket
from flask_socketio import SocketIO

from flask import Flask, jsonify, request, abort, redirect, url_for
from flask_cors import CORS

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def helloWorld():
    return "Hello, cross-origin-world!"


@app.route("/api/list-select", methods=['GET'])
def api_list_select():
    print("hello /api/list-select")

    return jsonify({
        'status': 'success',
    })
