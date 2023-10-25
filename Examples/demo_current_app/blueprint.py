from flask import Blueprint, current_app

sample = Blueprint('sample', __name__)


@sample.route('/')
def index():
    return current_app.config['SOMETHING']