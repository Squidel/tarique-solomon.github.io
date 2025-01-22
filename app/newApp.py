# from flask import Flask
# from dotenv import load_dotenv
# import os, logging
# from flask_sqlalchemy import SQLAlchemy

# logging.basicConfig(level=logging.DEBUG, filename='logs/debug.log', format='%(asctime)s %(levelname)s %(name)s : %(message)s')

# app = Flask(__name__)
# # CORS(app, origins='http://localhost:5001')
# load_dotenv()

# class Config:
#     DEBUG = False
#     SECRET_KEY = bytes.fromhex(os.getenv('SECRET_KEY_HEX'))

# # Development configuration
# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
#     #SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://localhost/PerformanceAppraisal?driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
    

# # Production configuration
# class ProductionConfig(Config):
#     DEBUG = False

# # Set configuration based on environment
# if os.getenv('ENVIRONMENT') == 'development':
#     app.config.from_object(DevelopmentConfig)
#     logging.info("Using development config")
# else:
#     app.config.from_object(ProductionConfig)
#     logging.info("Using production config")


# print("Database URL:", app.config['SQLALCHEMY_DATABASE_URI'])

# db = SQLAlchemy()
# db.init_app(app)
# # with app.app_context():
# #     db.reflect()

# # from controllers.adminController import AdminController
# # from controllers.appraisalController import AppraisalController
# # from controllers.employeeController import EmployeeController

# # app.register_blueprint(AdminController, url_prefix = '/api/admin')
# # app.register_blueprint(EmployeeController, url_prefix = '/api/employee')
# # app.register_blueprint(AppraisalController, url_prefix = '/api/appraisal')


# if __name__ == '__main__':
#     app.run(port=5000)
