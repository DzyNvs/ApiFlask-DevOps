from flask_restx import Namespace, Resource, fields
from Models.model_professores import listar_professores, professor_por_id, adicionar_professor, atualizar_professor, excluir_professor

professores_ns = Namespace("Professores", description="Operações relacionadas aos professores")

# Modelo de entrada para criação/atualização de professores
professor_model = professores_ns.model("Professor", {
    "nome": fields.String(required=True, description="Nome do professor"),
    "disciplina": fields.String(required=True, description="Especialidade do professor"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)"),
})

# Modelo de saída para listar e obter professores
professor_output_model = professores_ns.model("ProfessorOutput", {
    "id": fields.Integer(description="ID do professor"),
    "nome": fields.String(description="Nome do professor"),
    "idade": fields.Integer(description="Idade do professor calculada"),
    "data_nascimento": fields.String(description="Data de nascimento"),
    "disciplina": fields.String(description="Disciplina associada"),
})

@professores_ns.route("/")
class ProfessoresResource(Resource):
    @professores_ns.marshal_list_with(professor_output_model)
    def get(self):
        """Lista todos os professores"""
        return listar_professores()

    @professores_ns.expect(professor_model)
    @professores_ns.marshal_with(professor_output_model, code=201)
    def post(self):
        """Cria um novo professor"""
        data = professores_ns.payload
        return adicionar_professor(data)

@professores_ns.route("/<int:id_professor>")
class ProfessorIdResource(Resource):
    @professores_ns.marshal_with(professor_output_model)
    def get(self, id_professor):
        """Obtém um professor pelo ID"""
        return professor_por_id(id_professor)

    @professores_ns.expect(professor_model)
    @professores_ns.marshal_with(professor_output_model)
    def put(self, id_professor):
        """Atualiza um professor pelo ID"""
        data = professores_ns.payload
        return atualizar_professor(id_professor, data)  # Agora retorna diretamente o objeto atualizado

    def delete(self, id_professor):
        """Exclui um professor pelo ID"""
        return excluir_professor(id_professor)
