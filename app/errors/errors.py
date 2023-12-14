from flask import render_template
from flask import Blueprint

from app.models import db

error_blueprint = Blueprint('route_blueprint', __name__)

@error_blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@error_blueprint.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
