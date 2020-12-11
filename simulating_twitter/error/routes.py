from flask import Blueprint, render_template
from flask_login import login_required

error = Blueprint('error', __name__)

@error.errorhandler(404)
@login_required
def page_not_found(error_status):
    return render_template('404.html', error_status = 404)