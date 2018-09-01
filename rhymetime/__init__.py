from flask import Flask

def create_app():
    app = Flask(__name__)
    return app

APP = create_app()

from rhymetime import api
