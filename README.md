# Flask Web Application
This is a simple Web Application where the users can log in, view the data from their devices and control them.

## Application Breakdown
This is the breakdown of the web application. The current version uses [SQLite](https://www.sqlite.org/index.html) database
```
controller-platform
│   README.md
│   .gitignore
│   requirements.txt
│
└───flask_app
│   │   init.py
│   │   app.py
│   │   db.py
│   │   models.py
│   │
│   └───static
│   │   │   ...
│   │
│   └───templates
│   │   │   ...

```

## Flask Frameworks
These are the [Flask](http://flask.pocoo.org/docs/1.0/) libraries used in this Project. You'll find these in the requirements.txt file.
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
- [Flask-Login](https://flask-login.readthedocs.io/en/latest//)


## Deploying Locally
Lets walk through setting up your development environment and deploying this application on your local machine

1. Install Python, pip, and virtualenv
  - [Python](https://www.python.org/)
  - [pip](https://pip.pypa.io/en/stable/installing/)
  - [Virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

2. Clone this repo and CD into the projects directory
```
https://github.com/stsvetanov/controller-platform.git
cd solah-platform-mqtt
```
3. Create and activate a virtualenv
```
virtualenv venv
source venv/bin/activate
```
4. Install packages
```
pip install -r flask_app/requirements.txt
```

5. Run it
```
python3 flask_app/app.py
```