from flask import Flask
from config import Config


def create_app(config_class=Config):
    """Create a Flask application using the app factory pattern."""

    app = Flask(__name__)

    """Load configuration."""
    app.config.from_object(config_class)

    """Init app extensions."""
    from .extensions import db, login_manager, mqtt, socketio

    db.init_app(app)

    # login_manager.login_view = 'login'
    login_manager.init_app(app)

    mqtt.app = app
    mqtt.init_app(app)
    socketio.init_app(app)

    # """Register blueprints."""
    from .communication import bp as communication_bp
    app.register_blueprint(communication_bp)

    from .user import bp as user_bp
    app.register_blueprint(user_bp)

    from .data_view import bp as data_view_pb
    app.register_blueprint(data_view_pb)

    # from .errors import bp as errors_bp
    # app.register_blueprint(errors_bp)
    #
    # from .users import bp as users_bp
    # app.register_blueprint(users_bp, url_prefix='/users')

    # @app.route('/test/')
    # def test_page():
    #     return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
