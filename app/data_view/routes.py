import uuid

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models import BoilerTemp

bp = Blueprint('data_view', __name__)


# Shows real time incoming messages
@bp.route('/streaming_data')
@login_required
def streaming_data():
    # controller_id_hash = users_online_controller_id.get(current_user.controller_id)
    controller_id_hash = "my_topic_hash"
    return render_template('streaming_data.html', current_user=current_user, controller_id_hash=controller_id_hash)


# Shows static data from DB
@bp.route('/static_data')
@login_required
def static_data():
    print(current_user.controller_id)
    boiler_temp_data = BoilerTemp.query.filter_by(controller_id=current_user.controller_id).all()
    return render_template('static_data.html', boiler_temp_data=reversed(boiler_temp_data))