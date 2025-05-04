from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS

# Criação da instância do banco de dados
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Carrega as configurações da classe Config

    # Inicializa a extensão SQLAlchemy com a aplicação Flask
    db.init_app(app)

    with app.app_context():
        # Cria as tabelas no banco de dados
        db.create_all()

    return app

