from flask_restx import Namespace, Resource, fields
from Models.model_turmas import listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma

turmas_ns = Namespace("Turmas", description="Operações relacionadas às turmas")

# Modelo de entrada para criação/atualização de turmas
turma_model = turmas_ns.model("Turma", {
    "nome": fields.String(required=True, description="Nome da turma"),
    "materia": fields.String(required=True, description="Materia"),
    "descricao": fields.String(required=True, description="Descricao"),
    "ativo": fields.String(required=True, description="Ativo"),
    "turno": fields.String(required=True, description="Turno da turma"),
    "professor_id": fields.Integer(required=True, description="ID do professor associado"),
})

# Modelo de saída para listar e obter turmas
turma_output_model = turmas_ns.model("TurmaOutput", {
    "id": fields.Integer(description="ID da turma"),
    "nome": fields.String(description="Nome da turma"),
    "materia": fields.String(description="Materia"),
    "descricao": fields.String(description="Descrição"),
    "ativo": fields.String(description="Ativo"),
    "turno": fields.String(description="Turno da turma"),
    "professor_id": fields.Integer(description="ID do professor associado"),
})

@turmas_ns.route("/")
class TurmasResource(Resource):
    @turmas_ns.marshal_list_with(turma_output_model)
    def get(self):
        """Lista todas as turmas"""
        return listar_turmas()

    @turmas_ns.expect(turma_model)
    @turmas_ns.marshal_with(turma_output_model, code=201)
    def post(self):
        """Cria uma nova turma"""
        data = turmas_ns.payload
        return adicionar_turma(data), 201  # Agora sem desempacotamento incorreto
    
@turmas_ns.route("/<int:id_turma>")
class TurmasIdResource(Resource):
    @turmas_ns.marshal_with(turma_output_model)
    def get(self, id_turma):
        """Obtém uma turma pelo ID"""
        return turma_por_id(id_turma)

    @turmas_ns.expect(turma_model)
    @turmas_ns.marshal_with(turma_output_model)
    def put(self, id_turma):
        """Atualiza uma turma pelo ID"""
        data = turmas_ns.payload
        return atualizar_turma(id_turma, data), 200

    def delete(self, id_turma):
        """Exclui uma turma pelo ID"""
        return excluir_turma(id_turma), 200
