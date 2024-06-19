from dotenv import load_dotenv
load_dotenv()


import os

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') 
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_KEY') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False