import os

from dotenv import load_dotenv

load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-por-defecto')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', "sqlite:///default.db")
    
class Config_Test:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', "sqlite:///test.db")