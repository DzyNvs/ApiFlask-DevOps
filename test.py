
from flask import Flask, jsonify, request

app = Flask(__name__)

# Listas para armazenar os dados
alunos = []
professores = []
turmas = []

class AlunoNaoExiste(Exception):
    pass

@app.route('/', methods=['GET'])
def get_index():
    dados = {"msg": "Hello World!!!"}
    return jsonify(dados), 200

# Rotas para Alunos
@app.route("/alunos", methods=['GET'])
def get_alunos():
    return jsonify(alunos)

@app.route("/alunos", methods=['POST'])
def create_aluno():
    dados = request.json
    # Adiciona um novo aluno com um ID único
    dados['id'] = len(alunos) + 1
    alunos.append(dados)
    return jsonify(dados), 201

@app.route("/alunos/<int:id_aluno>", methods=['PUT'])
def update_aluno(id_aluno):
    for aluno in alunos:
        if aluno['id'] == id_aluno:
            dados = request.json
            aluno['nome'] = dados['nome']
            return jsonify(aluno), 200
    return jsonify({"msg": "Aluno não encontrado"}), 404

@app.route("/alunos/<int:id_aluno>", methods=['DELETE'])
def delete_aluno(id_aluno):
    global alunos
    for aluno in alunos:
        if aluno['id'] == id_aluno:
            alunos.remove(aluno)
            return jsonify({"msg": "Aluno removido com sucesso"}), 200
    return jsonify({"msg": "Aluno não encontrado"}), 404

# Rotas para Professores
@app.route("/professores", methods=['GET'])
def get_professores():
    return jsonify(professores)

@app.route("/professores", methods=['POST'])
def create_professor():
    dados = request.json
    dados['id'] = len(professores) + 1
    professores.append(dados)
    return jsonify(dados), 201

@app.route("/professores/<int:id_professor>", methods=['PUT'])
def update_professor(id_professor):
    for professor in professores:
        if professor['id'] == id_professor:
            dados = request.json
            professor['nome'] = dados['nome']
            return jsonify(professor), 200
    return jsonify({"msg": "Professor não encontrado"}), 404

@app.route("/professores/<int:id_professor>", methods=['DELETE'])
def delete_professor(id_professor):
    global professores
    for professor in professores:
        if professor['id'] == id_professor:
            professores.remove(professor)
            return jsonify({"msg": "Professor removido com sucesso"}), 200
    return jsonify({"msg": "Professor não encontrado"}), 404

# Rotas para Turmas
@app.route("/turmas", methods=['GET'])
def get_turmas():
    return jsonify(turmas)

@app.route("/turmas", methods=['POST'])
def create_turma():
    dados = request.json
    dados['id'] = len(turmas) + 1
    turmas.append(dados)
    return jsonify(dados), 201

@app.route("/turmas/<int:id_turma>", methods=['PUT'])
def update_turma(id_turma):
    for turma in turmas:
        if turma['id'] == id_turma:
            dados = request.json
            turma['descricao'] = dados['descricao']
            turma['professor_id'] = dados.get('professor_id', turma.get('professor_id'))
            turma['ativo'] = dados.get('ativo', turma.get('ativo'))
            return jsonify(turma), 200
    return jsonify({"msg": "Turma não encontrada"}), 404

@app.route("/turmas/<int:id_turma>", methods=['DELETE'])
def delete_turma(id_turma):
    global turmas
    for turma in turmas:
        if turma['id'] == id_turma:
            turmas.remove(turma)
            return jsonify({"msg": "Turma removida com sucesso"}), 200
    return jsonify({"msg": "Turma não encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)