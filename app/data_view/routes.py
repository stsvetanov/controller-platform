import uuid

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.models import BoilerTemp
from app.extensions import controller_id_to_hash

bp = Blueprint('data_view', __name__)


# Shows real time incoming messages
@bp.route('/streaming_data')
def streaming_data():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))

    controller_id_hash = controller_id_to_hash.get(current_user.controller_id)
    return render_template('streaming_data.html', current_user=current_user, controller_id_hash=controller_id_hash)


# Shows static data from DB
@bp.route('/static_data')
@login_required
def static_data():
    boiler_temp_data = (BoilerTemp.query
                        .filter_by(controller_id=current_user.controller_id)
                        .order_by(BoilerTemp.time_stamp.desc())
                        .limit(15)
                        # [:15]
                        # .all()
                        )
    return render_template('static_data.html', boiler_temp_data=boiler_temp_data)
