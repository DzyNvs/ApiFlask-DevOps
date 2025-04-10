from flask import Flask, jsonify, make_response, request 
from bd import alunos, professores, turmas, add_aluno, add_professor, add_turma

ap = Flask(__name__)
ap.config['JSON_SORT_KEYS'] = False

#RESETA

@ap.route('/reseta', methods=['POST'])
def resetar_dados():
    # Limpa todas as listas
    alunos.clear()
    professores.clear()
    turmas.clear()

    return make_response(jsonify({"mensagem": "Dados resetados com sucesso"}), 200)


#aLUNOS
# CREaTE ALUNO (POST)
@ap.route('/alunos', methods=['POST'])
def create_alunos():
    dados = request.json

    # Verificar campos obrigatórios, incluindo professor_id
    campos_obrigatorios = [
        'nome', 
        'data_nascimento', 
        'nota_primeiro_semestre', 
        'nota_segundo_semestre', 
        'turma_id',
        'professor_id'
    ]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return make_response(
                jsonify({"erro": f"Campo obrigatório '{campo}' está faltando"}), 
                400
            )

    # Verificar se o professor existe
    professor = get_professor_by_id(dados['professor_id'])
    if not professor:
        return make_response(
            jsonify({"erro": "professor com o ID fornecido não existe"}), 
            404
        )

    # adicionar o aluno (simulando o banco de dados)
    novo_aluno = add_aluno(
        nome=dados['nome'],
        data_nascimento=dados['data_nascimento'],
        nota_primeiro_semestre=dados['nota_primeiro_semestre'],
        nota_segundo_semestre=dados['nota_segundo_semestre'],
        turma_id=dados['turma_id'],
        professor_id=dados['professor_id']
    )

    return make_response(jsonify(novo_aluno), 201)


#LISTa aLUNOS(GET)
@ap.route('/alunos', methods=['GET'])
def get_alunos():
    return make_response (jsonify(alunos)),200

#pROCURa ALUNO POR ID(GET BY ID)
@ap.route('/alunos/<int:id>', methods=['GET'])
def get_aluno(id):
    aluno = next((a for a in alunos if a['id']==id), None)
    if aluno: 
        return make_response(jsonify({'id': aluno['id'], 'nome': aluno['nome'], 'data_nascimento': aluno['data_nascimento'], 'nota_primeiro_semestre': aluno['nota_primeiro_semestre'], 'nota_segundo_semestre': aluno['nota_segundo_semestre'], 'turma_id': aluno['turma_id'] })),200
    return make_response(jsonify({"erro": "aluno não encontrado" })), 404

#EXCLUI ALUNO pOR ID(DELETE BY ID)
@ap.route('/alunos/<int:id>', methods=['DELETE'])
def deletar_aluno_por_id(id):
        global alunos
        aluno = next((a for a in alunos if a['id'] == id), None)
        if aluno:
            alunos.remove(aluno)
            return make_response(jsonify({"mensagem": f"aluno com ID {id} deletado"}), 200)
        return make_response(jsonify({"erro": "aluno não encontrado"}), 404)
             


#EDITa ALUNO POR ID(PUT)
@ap.route('/alunos/<int:id>', methods=['PUT'])
def editar_aluno(id):
    aluno = next((a for a in alunos if a['id'] == id), None)

    if not aluno:
        return make_response(jsonify({"erro": "aluno não encontrado"}), 404)

    dados = request.json

    aluno['nome'] = dados.get('nome', aluno['nome'])
    aluno['data_nascimento'] = dados.get('data_nascimento', aluno['data_nascimento'])
    aluno['nota_primeiro_semestre'] = dados.get('nota_primeiro_semestre', aluno['nota_primeiro_semestre'])
    aluno['nota_segundo_semestre'] = dados.get('nota_segundo_semestre', aluno['nota_segundo_semestre'])
    aluno['turma_id'] = dados.get('turma_id', aluno['turma_id'])

    return make_response(jsonify({"mensagem": f"aluno com ID {id} atualizado com sucesso"}), 200)


#professores 
#CREaTE pROFESSOR(POST)
@ap.route('/professores', methods=['POST'])
def create_professores():
    dados = request.json

    # Chamando a função do bd.py para adicionar o professor
    novo_professor = add_professor(
        nome=dados['nome'],
        idade=dados['idade'],
        data_nascimento=dados['data_nascimento'],
        disciplina=dados['disciplina'],
        salario=dados['salario']
    )

    return make_response(jsonify(novo_professor), 201)


#LISTa pROFESSORES(GET)
@ap.route('/professores', methods=['GET'])
def get_professores():
    return make_response (jsonify(professores)),200

#pROCURa pROFESSOR pOR ID(POST BY ID)
@ap.route('/professores/<int:id>', methods=['GET'])
def get_professor_by_id(professor_id):
    for professor in professores:
        if professor["id"] == professor_id:
            return professor
    return None

#EXCLUI pROFESSOR pOR ID(DELETE BY ID)
@ap.route('/professores/<int:id>', methods=['DELETE'])
def deletar_professor_por_id(id):
    global professores
    professor = next((p for p in professores if p ['id']==id), None)
    if professor: 
        professores.remove(professor)
        return make_response(jsonify({"mensagem": f"professor com ID {id} deletado"})),200
    return make_response(jsonify({"erro": 'professor não encontrado'})), 400

#EDITa pROFESSOR pOR ID(PUT BY ID)
@ap.route('/professores/<int:id>', methods=['PUT'])
def editar_professor(id):
    professor = next((p for p in professores if p['id'] == id), None)

    if not professor:
        return make_response(jsonify({"erro": "professor não encontrado"}), 404)

    dados = request.json

    professor['nome'] = dados.get('nome', professor['nome'])
    professor['idade'] = dados.get('idade', professor['idade'])
    professor['data_nascimento'] = dados.get('data_nascimento', professor['data_nascimento'])
    professor['disciplina'] = dados.get('disciplina', professor['disciplina'])
    professor['salario'] = dados.get('salario', professor['salario'])

    return make_response(jsonify({"mensagem": f"professor com ID {id} atualizado com sucesso"})), 200


#turmas
#CREaTE turmas(POST)
@ap.route('/turmas', methods=['POST'])
def criar_turma():
    if not request.json:
        return jsonify({"erro": "Dados inválidos ou ausentes"}), 400

    dados = request.json

    # Verifica se os campos obrigatórios estão presentes
    campos_obrigatorios = ['nome', 'turno', 'professor_id']
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios: nome, turno, professor_id"}), 400

    try:
        nova_turma = add_turma(
            nome=dados['nome'],
            turno=dados['turno'],
            professor_id=dados['professor_id']
        )
        return jsonify(nova_turma), 201  # Retorna a nova turma criada com status 201
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar turma: {str(e)}"}), 500


#LISTa turmas(GET)
@ap.route('/turmas', methods=['GET'])
def get_turmas():
    return make_response (jsonify(turmas))

#pROCURa TURMa pOR ID(GET BY ID)
@ap.route('/turmas/<int:id>', methods=['GET'])
def get_Turma(id):
    turma = next((t for t in turmas if t['id']==id), None)
    if turma: 
        return make_response(jsonify({'id': turma['id'], 'nome': turma['nome'], 'turno': turma['turno'], 'professor_id': turma['professor_id']})),200
    return make_response(jsonify({"erro": "Turma não encontrada" })), 404


#EXCLUI TURMa pELO ID(DELETE BY ID)
@ap.route('/turmas/<int:id>', methods=['DELETE'])
def deletar_turma_por_id(id):
    global turmas
    turma = next((t for t in turmas if t ['id']==id), None)
    if turma: 
        turmas.remove(turma)
        return make_response(jsonify({"mensagem": f"Turma com ID {id} deletado"})),200
    return make_response(jsonify({"erro": 'Turma não encontrada'})), 400

#EDITa TURMa pOR ID(PUT BY ID)
@ap.route('/turmas/<int:id>', methods=['PUT'])
def editar_turmas(id):
    turma = next((t for t in turmas if t['id'] == id), None)

    if not turma:
        return make_response(jsonify({"erro": "Turma não encontrada"}), 404)

    dados = request.json

    turma['nome'] = dados.get('nome', turma['nome'])
    turma['turno'] = dados.get('turno', turma['turno'])
    turma['professor_id'] = dados.get('professor_id', turma['professor_id'])


    return make_response(jsonify({"mensagem": f"Turma com ID {id} atualizado com sucesso"})), 200



if __name__  == '__main__': 
    ap.run(debug=True)