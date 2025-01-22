from app import create_app
from flask import render_template
from flask_login import LoginManager
from app.database.models.models import Users

app = create_app()

    
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Utility function to get routes for a specific blueprint
def get_routes_for_blueprint(blueprint_name):
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith(blueprint_name):
            routes.append({
                'endpoint': rule.endpoint,
                'url': rule.rule
            })
    return routes

if __name__ == '__main__':
    app.run(port=5000)