from flask import Flask, jsonify, make_response, request 
from bd import Alunos, Professores, Turmas, add_aluno, add_professor, add_turma

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#RESETA

@app.route('/reseta', methods=['POST'])
def resetar_dados():
    # Limpa todas as listas
    Alunos.clear()
    Professores.clear()
    Turmas.clear()

    return make_response(jsonify({"mensagem": "Dados resetados com sucesso"}), 200)


#ALUNOS
#CREATE ALUNO(POST)
@app.route('/Alunos', methods=['POST'])
def create_Alunos():
    dados = request.json

    # Verificar campos obrigatórios
    campos_obrigatorios = ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id']
    for campo in campos_obrigatorios:
        if campo not in dados:
            return make_response(jsonify({"erro": f"Campo obrigatório '{campo}' está faltando"}), 400)

    # Adicionar o aluno (simulando o banco de dados)
    novo_aluno = add_aluno(
        nome=dados['nome'],
        data_nascimento=dados['data_nascimento'],
        nota_primeiro_semestre=dados['nota_primeiro_semestre'],
        nota_segundo_semestre=dados['nota_segundo_semestre'],
        turma_id=dados['turma_id']
    )

    return make_response(jsonify(novo_aluno), 201)


#LISTA ALUNOS(GET)
@app.route('/Alunos', methods=['GET'])
def get_Alunos():
    return make_response (jsonify(Alunos)),200

#PROCURA ALUNO POR ID(GET BY ID)
@app.route('/Alunos/<int:id>', methods=['GET'])
def get_Aluno(id):
    aluno = next((a for a in Alunos if a['id']==id), None)
    if aluno: 
        return make_response(jsonify({'id': aluno['id'], 'nome': aluno['nome'], 'data_nascimento': aluno['data_nascimento'], 'nota_primeiro_semestre': aluno['nota_primeiro_semestre'], 'nota_segundo_semestre': aluno['nota_segundo_semestre'], 'turma_id': aluno['turma_id'] })),200
    return make_response(jsonify({"erro": "Aluno não encontrado" })), 404

#EXCLUI ALUNO POR ID(DELETE BY ID)

@app.route('/Alunos/<int:id>', methods=['DELETE'])
def deletar_aluno_por_id(id):
        global Alunos
        aluno = next((a for a in Alunos if a['id'] == id), None)
        if aluno:
            Alunos.remove(aluno)
            return make_response(jsonify({"mensagem": f"Aluno com ID {id} deletado"}), 200)
        return make_response(jsonify({"erro": "Aluno não encontrado"}), 404)
             


#EDITA ALUNO POR ID(PUT)
@app.route('/Alunos/<int:id>', methods=['PUT'])
def editar_Aluno(id):
    aluno = next((a for a in Alunos if a['id'] == id), None)

    if not aluno:
        return make_response(jsonify({"erro": "Aluno não encontrado"}), 404)

    dados = request.json

    aluno['nome'] = dados.get('nome', aluno['nome'])
    aluno['data_nascimento'] = dados.get('data_nascimento', aluno['data_nascimento'])
    aluno['nota_primeiro_semestre'] = dados.get('nota_primeiro_semestre', aluno['nota_primeiro_semestre'])
    aluno['nota_segundo_semestre'] = dados.get('nota_segundo_semestre', aluno['nota_segundo_semestre'])
    aluno['turma_id'] = dados.get('turma_id', aluno['turma_id'])

    return make_response(jsonify({"mensagem": f"Aluno com ID {id} atualizado com sucesso"}), 200)


#Professores 
#CREATE PROFESSOR(POST)
@app.route('/Professores', methods=['POST'])
def create_Professores():
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


#LISTA PROFESSORES(GET)
@app.route('/Professores', methods=['GET'])
def get_Professores():
    return make_response (jsonify(Professores)),200

#PROCURA PROFESSOR POR ID(POST BY ID)
@app.route('/Professores/<int:id>', methods=['GET'])
def get_Professor(id):
    professor = next((p for p in Professores if p['id']==id), None)
    if professor: 
        return make_response(jsonify({'id': professor['id'], 'nome': professor['nome'], 'idade': professor['idade'], 'data_nascimento': professor['data_nascimento'], 'disciplina': professor['disciplina'], 'salario': professor['salario']})),200
    return make_response(jsonify({"erro": "Professor não encontrado" })), 404

#EXCLUI PROFESSOR POR ID(DELETE BY ID)
@app.route('/Professores/<int:id>', methods=['DELETE'])
def deletar_professor_por_id(id):
    global Professores
    professor = next((p for p in Professores if p ['id']==id), None)
    if professor: 
        Professores.remove(professor)
        return make_response(jsonify({"mensagem": f"Professor com ID {id} deletado"})),200
    return make_response(jsonify({"erro": 'Professor não encontrado'})), 400

#EDITA PROFESSOR POR ID(PUT BY ID)
@app.route('/Professores/<int:id>', methods=['PUT'])
def editar_Professor(id):
    professor = next((p for p in Professores if p['id'] == id), None)

    if not professor:
        return make_response(jsonify({"erro": "Professor não encontrado"}), 404)

    dados = request.json

    professor['nome'] = dados.get('nome', professor['nome'])
    professor['idade'] = dados.get('idade', professor['idade'])
    professor['data_nascimento'] = dados.get('data_nascimento', professor['data_nascimento'])
    professor['disciplina'] = dados.get('disciplina', professor['disciplina'])
    professor['salario'] = dados.get('salario', professor['salario'])

    return make_response(jsonify({"mensagem": f"Professor com ID {id} atualizado com sucesso"})), 200


#Turmas
#CREATE TURMAS(POST)
@app.route('/Turmas', methods=['POST'])
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


#LISTA TURMAS(GET)
@app.route('/Turmas', methods=['GET'])
def get_Turmas():
    return make_response (jsonify(Turmas))

#PROCURA TURMA POR ID(GET BY ID)
@app.route('/Turmas/<int:id>', methods=['GET'])
def get_Turma(id):
    turma = next((t for t in Turmas if t['id']==id), None)
    if turma: 
        return make_response(jsonify({'id': turma['id'], 'nome': turma['nome'], 'turno': turma['turno'], 'professor_id': turma['professor_id']})),200
    return make_response(jsonify({"erro": "Turma não encontrada" })), 404


#EXCLUI TURMA PELO ID(DELETE BY ID)
@app.route('/Turmas/<int:id>', methods=['DELETE'])
def deletar_turma_por_id(id):
    global Turmas
    turma = next((t for t in Turmas if t ['id']==id), None)
    if turma: 
        Turmas.remove(turma)
        return make_response(jsonify({"mensagem": f"Turma com ID {id} deletado"})),200
    return make_response(jsonify({"erro": 'Turma não encontrada'})), 400

#EDITA TURMA POR ID(PUT BY ID)
@app.route('/Turmas/<int:id>', methods=['PUT'])
def editar_Turmas(id):
    turma = next((t for t in Turmas if t['id'] == id), None)

    if not turma:
        return make_response(jsonify({"erro": "Turma não encontrada"}), 404)

    dados = request.json

    turma['nome'] = dados.get('nome', turma['nome'])
    turma['turno'] = dados.get('turno', turma['turno'])
    turma['professor_id'] = dados.get('professor_id', turma['professor_id'])


    return make_response(jsonify({"mensagem": f"Turma com ID {id} atualizado com sucesso"})), 200



if __name__  == '__main__': 
    app.run(debug=True)