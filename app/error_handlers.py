from flask import jsonify, render_template, make_response, abort, redirect, url_for, g
from app import logging
from flask_login import current_user
from functools import wraps

def set_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        logging.error(f'Page not found: {error}')
        return render_template('404.html'),404
    @app.errorhandler(500)
    def internal_error(error):
        logging.error(f'Internal server found: {error}')
        return jsonify({
            'message': 'An internal server error occurred.',
            'status': 'error'
        }), 500
    @app.before_request
    def load_logged_in_user():
        g.user = current_user
    
# Decorator for role-based access control
def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def wrapped_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('main.login'))  # Redirect to login if user is not authenticated
            logging.info(f'role info: {vars(current_user)} and required roles: {required_role}')
            roles = required_role.split(',')
            user_roles = current_user.role.split(',')
            has_role = [x for x in roles if x in user_roles]
            logging.info(f"required roles: {roles}; user roles: {user_roles} does the user have a required role: {not has_role} is admin in user roles: {'admin' not in user_roles}")
            if not has_role and 'admin' not in user_roles:
                abort(403)  # Forbidden if user doesn't have the required role
            return fn(*args, **kwargs)
        return wrapped_view
    return wrapper


