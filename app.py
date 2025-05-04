from bd import create_app, db  # Importando a função create_app
from Controllers.alunos_routes import alunos_blueprint
from Controllers.professores_routes import professores_blueprint
from Controllers.turmas_routes import turmas_blueprint
from swagger.swagger_config import configure_swagger

app = create_app()  # Cria a instância da aplicação

with app.app_context():
    db.create_all()
# Registro dos Blueprints
app.register_blueprint(alunos_blueprint, url_prefix='/api/alunos')
app.register_blueprint(professores_blueprint, url_prefix='/api/professores')
app.register_blueprint(turmas_blueprint, url_prefix='/api/turmas')

configure_swagger(app)

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config['PORT'], debug=app.config['DEBUG'])