import os

class Config:
    HOST = '127.0.0.1'
    PORT = 5000
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///bd_sql.db"  # Exemplo usando SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desativa o rastreamento de modificações