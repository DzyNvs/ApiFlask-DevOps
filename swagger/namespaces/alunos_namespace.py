from flask_restx import Namespace, Resource, fields
from Models.model_alunos import listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno

alunos_ns = Namespace("Alunos", description="Operações relacionadas a alunos")

aluno_model = alunos_ns.model("Aluno", {
    "nome": fields.String(required=True, description="Nome do aluno"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento"),
    "nota_primeiro_semestre": fields.Float(required=True),
    "nota_segundo_semestre": fields.Float(required=True),
    "turma_id": fields.Integer(required=True)
})

aluno_output_model = alunos_ns.model("AlunoOutput", {
    "id": fields.Integer(description="ID do aluno"),
    "nome": fields.String(description="Nome do aluno"),
    "idade": fields.Integer(description="Idade do aluno calculada"),
    "data_nascimento": fields.String(description="Data de nascimento (YYYY-MM-DD)"),
    "nota_primeiro_semestre": fields.Float(description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(description="Nota do segundo semestre"),
    "media_final": fields.Float(description="Média final do aluno"),
    "turma_id": fields.Integer(description="ID da turma associada"),
})

@alunos_ns.route("/")
class AlunosResource(Resource):
    @alunos_ns.marshal_list_with(aluno_output_model)
    def get(self):
        """Lista todos os alunos"""
        return listar_alunos()

    @alunos_ns.expect(aluno_model)
    @alunos_ns.marshal_with(aluno_output_model, code=201)
    def post(self):
        """Cria um novo aluno"""
        data = alunos_ns.payload
        return adicionar_aluno(data)

@alunos_ns.route("/<int:id_aluno>")
class AlunoIdResource(Resource):
    @alunos_ns.marshal_with(aluno_output_model)
    def get(self, id_aluno):
        """Obtém um aluno pelo ID"""
        return aluno_por_id(id_aluno)

    @alunos_ns.expect(aluno_model)
    @alunos_ns.marshal_with(aluno_output_model)
    def put(self, id_aluno):
        """Atualiza um aluno pelo ID"""
        data = alunos_ns.payload
        return atualizar_aluno(id_aluno, data), 200

    def delete(self, id_aluno):
        """Exclui um aluno pelo ID"""
        return excluir_aluno(id_aluno), 200
