from flask import Flask


def create_app():
    """
    creates our flask app
    :return:
    """
    flask_app = Flask(__name__)
    return flask_app
