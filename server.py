import os
import eventlet
from eventlet import wsgi

from app import create_app
# app = create_app(os.getenv("ENV", "development"))
app = create_app()

if __name__ == "__main__":
    app.run()
    # wsgi.server(eventlet.listen(('', 5000)), app, debug=True)

