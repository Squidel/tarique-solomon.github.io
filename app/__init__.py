from flask import Flask
from dotenv import load_dotenv
import os, logging
from flask_sqlalchemy import SQLAlchemy
from app.app_config import DevelopmentConfig, ProductionConfig
from app.error_handlers import set_error_handlers
from flask_login import LoginManager


import sqlite3

logging.basicConfig(level=logging.DEBUG, filename='logs/debug.log', format='%(asctime)s %(levelname)s %(name)s : %(message)s')

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # CORS(app, origins='http://localhost:5001')
    load_dotenv()
    
    # Set configuration based on environment
    if os.getenv('ENVIRONMENT') == 'development':
        app.config.from_object(DevelopmentConfig)
        logging.info("Using development config")
    else:
        app.config.from_object(ProductionConfig)
        logging.info("Using production config")


    print("Database URL:", app.config['SQLALCHEMY_DATABASE_URI'])
    
    db.init_app(app)
    # with app.app_context():
    #     # Create tables if they don't exist
    #     db.create_all()
    
    from app.routes.routes import promotions_bp, admin_bp, index_bp
    from app.api.api import api_bp
    app.register_blueprint(promotions_bp, url_prefix='/blog')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(index_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    set_error_handlers(app)
    print(app.template_folder)
    return app