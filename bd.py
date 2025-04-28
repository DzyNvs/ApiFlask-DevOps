from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

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

# Definição dos modelos
class Aluno(db.Model):
    __tablename__ = 'alunos'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(100), nullable=False)  # Nome do aluno
    idade = db.Column(db.Integer)  # Idade do aluno
    data_nascimento = db.Column(db.String(10), nullable=False)  # Data de nascimento
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)  # Nota do primeiro semestre
    nota_segundo_semestre = db.Column(db.Float, nullable=False)  # Nota do segundo semestre
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'))  # Chave estrangeira para turmas
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))  # Chave estrangeira para professores

class Professor(db.Model):
    __tablename__ = 'professores'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(100), nullable=False)  # Nome do professor
    idade = db.Column(db.Integer)  # Idade do professor
    data_nascimento = db.Column(db.String(10), nullable=False)  # Data de nascimento
    disciplina = db.Column(db.String(100), nullable=False)  # Disciplina que leciona
    salario = db.Column(db.Float, nullable=False)  # Salário do professor

class Turma(db.Model):
    __tablename__ = 'turmas'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(100), nullable=False)  # Nome da turma
    turno = db.Column(db.String(50), nullable=False)  # Turno da turma
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))  # Chave estrangeira para professores

    # Relacionamentos
    alunos = db.relationship('Aluno', backref='turma', lazy=True)  # Relacionamento com Aluno