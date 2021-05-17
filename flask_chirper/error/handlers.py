from flask import Blueprint, render_template


error = Blueprint('error', __name__)


# .errorhandler will only be active within this blueprint
# whereas .app_errorhandler works across the entire application
@error.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@error.app_errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403


@error.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
