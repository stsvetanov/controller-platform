# Flask Web Application
This is a simple Web Application where the users can log in, view the data from their devices and control them.

## Application Breakdown
This is the breakdown of the web application. The current version uses [SQLite](https://www.sqlite.org/index.html) database
```
controller-platform
│   README.md
│   .gitignore
│   requirements.txt
|   wsgi.py
│
└───flask_app
│   │   __init__.py
│   │   app.py
│   │   db.py
│   │   models.py
│   │
│   └───templates
│   │   │   ...

```

## Flask Frameworks
These are some of the [Flask](https://flask.palletsprojects.com/en/1.1.x/) libraries used in this Project. You'll find these in the requirements.txt file.
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Flask-Login](https://flask-login.readthedocs.io/en/latest//)


## Deploying Locally
Lets walk through setting up your development environment and deploying this application on your local machine

1. Install Python, pip, and virtualenv
  - [Python](https://www.python.org/)
  - [pip](https://pip.pypa.io/en/stable/installing/)
  - [Virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

2. Clone this repo and CD into the projects directory
```
https://github.com/stsvetanov/controller-platform.git controller-platform
cd controller-platform
```
3. Create and activate a virtualenv
```
virtualenv venv
source venv/bin/activate
```
4. Install packages
```
pip install -r requirements.txt
```

5. Run it
```
python3 wsgi.py
```