from flask import Flask, jsonify, make_response, request 
from bd import Alunos, Professores, Turmas

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#ALUNOS
@app.route('/Alunos', methods=['POST'])
def create_Alunos():
    alunos = request.json
    Alunos.append(alunos)   
    return make_response (jsonify(Alunos))


 

@app.route('/Alunos', methods=['GET'])
def get_Alunos():
    return make_response (jsonify(Alunos))


@app.route('/Alunos/<int:id>', methods=['GET'])
def get_Aluno(id):
    aluno = next((a for a in Alunos if a['id']==id), None)
    if aluno: 
        return make_response(jsonify({'id': aluno['id'], 'nome': aluno['nome']})),200
    return make_response(jsonify({"erro": "Aluno não encontrado" })), 404

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



@app.route('/Alunos/<int:id>', methods=['PUT'])
def editar_Alunos(id):
    aluno = next((a for a in Alunos if a['id'] == id), None)

    if not aluno:
        return make_response(jsonify({"message": "Aluno não encontrado"}), 404)

    nome_novo = request.form.get('nome')

    if not nome_novo:
        return make_response(jsonify({"erro": "Campo 'nome' é obrigatório"}), 400)

    aluno["nome"] = nome_novo

    return make_response(jsonify({"mensagem": f"Aluno com ID {id} atualizado para {aluno['nome']}"}), 200)



#Professores 

@app.route('/Professores', methods=['POST'])
def create_Professores():
    professores = request.json
    Professores.append(professores)   
    return make_response (jsonify(Professores))

@app.route('/Professores', methods=['GET'])
def get_Professores():
    return make_response (jsonify(Professores))

@app.route('/Professores/<int:id>', methods=['GET'])
def get_Professor(id):
    professor = next((p for p in Professores if p['id']==id), None)
    if professor: 
        return make_response(jsonify({'id': professor['id'], 'nome': professor['nome']})),200
    return make_response(jsonify({"erro": "Professor não encontrado" })), 404

@app.route('/Professores/<int:id>', methods=['DELETE'])
def deletar_professor_por_id(id):
    global Professores
    professor = next((p for p in Professores if p ['id']==id), None)
    if professor: 
        Professores.remove(professor)
        return make_response(jsonify({"mensagem": f"Professor com ID {id} deletado"})),200
    return make_response(jsonify({"erro": 'Professor não encontrado'})), 400

#Turmas

@app.route('/Turmas', methods=['POST'])
def create_Turmas():
    turmas = request.json
    Turmas.append(turmas)   
    return make_response (jsonify(Turmas))

@app.route('/Turmas', methods=['GET'])
def get_Turmas():
    return make_response (jsonify(Turmas))

@app.route('/Turmas/<int:id>', methods=['GET'])
def get_Turma(id):
    turma = next((t for t in Professores if t['id']==id), None)
    if turma: 
        return make_response(jsonify({'id': turma['id'], 'nome': turma['nome']})),200
    return make_response(jsonify({"erro": "Turma não encontrada" })), 404

@app.route('/Turmas/<int:id>', methods=['DELETE'])
def deletar_turma_por_id(id):
    global Turmas
    turma = next((t for t in Turmas if t ['id']==id), None)
    if turma: 
        Turmas.remove(turma)
        return make_response(jsonify({"mensagem": f"Turma com ID {id} deletado"})),200
    return make_response(jsonify({"erro": 'Turma não encontrada'})), 400



if __name__  == '__main__': 
    app.run(debug=True)