from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import User

app = create_app()
with app.app_context():
    db.create_all()
    db.session.commit()

    user = User.query.first()
    if not user:
        user_1 = User(email="user1@mail.com", controller_id=1, password=generate_password_hash("password", method='scrypt', salt_length=16))
        user_2 = User(email="user2@mail.com", controller_id=2, password=generate_password_hash("password", method='scrypt', salt_length=16))
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()
