import uuid
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import User
from app.extensions import login_manager


bp = Blueprint('user', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # if not (user and check_password_hash(user.password, password)):
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('user.login'))

    login_user(user, remember=remember)

    # global users_online_controller_id
    # controller_id_hash = uuid.uuid4().hex
    # users_online_controller_id[current_user.controller_id] = controller_id_hash

    return redirect(url_for('user.profile'))


@bp.route('/logout')
@login_required
def logout():
    # global users_online_controller_id
    # if users_online_controller_id.get(current_user.controller_id):
    #     del users_online_controller_id[current_user.controller_id]
    logout_user()
    return redirect(url_for('user.index'))
