import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'ugc.db')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    DJANGO_API_URL = "http://localhost:8000"
    
    SECRET_KEY = "ugc-secret-key-change-in-production"

    DEBUG = True