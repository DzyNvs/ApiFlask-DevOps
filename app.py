from flask import Flask
from Controllers.alunos_routes import alunos_blueprint
from Controllers.professores_routes import professores_blueprint
from Controllers.turmas_routes import turmas_blueprint

app = Flask(__name__)

# Registro dos Blueprints
app.register_blueprint(alunos_blueprint)
app.register_blueprint(professores_blueprint)
app.register_blueprint(turmas_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
