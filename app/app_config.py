from dotenv import load_dotenv
import os, logging

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

class Config:
    DEBUG = False
    SECRET_KEY = bytes.fromhex(os.getenv('SECRET_KEY_HEX'))
    
    #actual values
    settings = None
    
    def init_config(app):
        Config.settings = app.config


# Development configuration
class DevelopmentConfig(Config):
    DEBUG = True
    IsSQlite = False
    db_path = os.getenv('DATABASE_URL')
    if(os.getenv('IsSQLite')== 'True'):
        IsSQlite = True
        basedir = os.path.abspath(os.path.dirname(__file__))  # Base directory of your project
        path = os.path.join(basedir, os.getenv('DATABASE_URL'))
        db_path = f"sqlite:///{path.replace('\\', '/')}"
    SQLALCHEMY_DATABASE_URI = db_path
    #SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://localhost/PerformanceAppraisal?driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

# Production configuration
class ProductionConfig(Config):
    DEBUG = False             

#Secret Key Process

secret_key_hex = os.getenv('SECRET_KEY_HEX')
secret_key = bytes.fromhex(secret_key_hex) # Convert the hexadecimal string back to bytes

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif', 'heic'}
UPLOADS_FOLDER = os.path.join(os.getcwd(), 'uploads')
WINNER_RATIO = 2
