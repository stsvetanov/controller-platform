import eventlet
from eventlet import wsgi

"""Application entry point."""
from flask_app import app

if __name__ == "__main__":
    wsgi.server(eventlet.listen(('', 5000)), app, debug=True)

