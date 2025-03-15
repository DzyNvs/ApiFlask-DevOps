from flask import Flask, jsonify, request
from models import Aluno, Professor, Turma

app = Flask(__name__)

# Dados fictícios para simulação
alunos = []
professores = []
turmas = []

# CRUD para Alunos
@app.route('/api/alunos/', methods=['GET'])
def get_alunos():
    return jsonify([aluno.__dict__ for aluno in alunos]), 200

@app.route('/api/alunos/', methods=['POST'])
def create_aluno():
    data = request.get_json()
    aluno = Aluno(**data)
    aluno.id = len(alunos) + 1
    aluno.media_final = aluno.calcular_media()  # Calculando a média ao criar o aluno
    alunos.append(aluno)
    return jsonify(aluno.__dict__), 200

@app.route('/api/alunos/<int:id_aluno>/', methods=['GET'])
def get_aluno(id_aluno):
    aluno = next((a for a in alunos if a.id == id_aluno), None)
    if aluno:
        return jsonify(aluno.__dict__), 200
    return jsonify({'message': 'Aluno não encontrado'}), 404

@app.route('/api/alunos/<int:id_aluno>/', methods=['PUT'])
def update_aluno(id_aluno):
    data = request.get_json()
    aluno = next((a for a in alunos if a.id == id_aluno), None)
    if aluno:
        aluno.nome = data.get('nome', aluno.nome)
        aluno.idade = data.get('idade', aluno.idade)
        aluno.turma_id = data.get('turma_id', aluno.turma_id)
        aluno.data_nascimento = data.get('data_nascimento', aluno.data_nascimento)
        aluno.nota_primeiro_semestre = data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
        aluno.nota_segundo_semestre = data.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
        aluno.media_final = aluno.calcular_media()  # Recalcula a média
        return jsonify(aluno.__dict__), 200
    return jsonify({'message': 'Aluno não encontrado'}), 404

@app.route('/api/alunos/<int:id_aluno>/', methods=['DELETE'])
def delete_aluno(id_aluno):
    aluno = next((a for a in alunos if a.id == id_aluno), None)
    if aluno:
        alunos.remove(aluno)
        return jsonify({'message': 'Aluno excluído'}), 200
    return jsonify({'message': 'Aluno não encontrado'}), 404

# CRUD para Professores
@app.route('/api/professores/', methods=['GET'])
def get_professores():
    return jsonify([professor.__dict__ for professor in professores]), 200

@app.route('/api/professores/', methods=['POST'])
def create_professor():
    data = request.get_json()
    professor = Professor(**data)
    professor.id = len(professores) + 1
    professores.append(professor)
    return jsonify(professor.__dict__), 200

@app.route('/api/professores/<int:id_professor>/', methods=['GET'])
def get_professor(id_professor):
    professor = next((p for p in professores if p.id == id_professor), None)
    if professor:
        return jsonify(professor.__dict__), 200
    return jsonify({'message': 'Professor não encontrado'}), 404

@app.route('/api/professores/<int:id_professor>/', methods=['PUT'])
def update_professor(id_professor):
    data = request.get_json()
    professor = next((p for p in professores if p.id == id_professor), None)
    if professor:
        professor.nome = data.get('nome', professor.nome)
        professor.idade = data.get('idade', professor.idade)
        professor.materia = data.get('materia', professor.materia)
        professor.observacoes = data.get('observacoes', professor.observacoes)
        return jsonify(professor.__dict__), 200
    return jsonify({'message': 'Professor não encontrado'}), 404

@app.route('/api/professores/<int:id_professor>/', methods=['DELETE'])
def delete_professor(id_professor):
    professor = next((p for p in professores if p.id == id_professor), None)
    if professor:
        professores.remove(professor)
        return jsonify({'message': 'Professor excluído'}), 200
    return jsonify({'message': 'Professor não encontrado'}), 404

# CRUD para Turmas
@app.route('/api/turmas/', methods=['GET'])
def get_turmas():
    return jsonify([turma.__dict__ for turma in turmas]), 200

@app.route('/api/turmas/', methods=['POST'])
def create_turma():
    data = request.get_json()
    turma = Turma(**data)
    turma.id = len(turmas) + 1
    turmas.append(turma)
    return jsonify(turma.__dict__), 200

@app.route('/api/turmas/<int:id_turma>/', methods=['GET'])
def get_turma(id_turma):
    turma = next((t for t in turmas if t.id == id_turma), None)
    if turma:
        return jsonify(turma.__dict__), 200
    return jsonify({'message': 'Turma não encontrada'}), 404

@app.route('/api/turmas/<int:id_turma>/', methods=['PUT'])
def update_turma(id_turma):
    data = request.get_json()
    turma = next((t for t in turmas if t.id == id_turma), None)
    if turma:
        turma.descricao = data.get('descricao', turma.descricao)
        turma.professor_id = data.get('professor_id', turma.professor_id)
        turma.ativo = data.get('ativo', turma.ativo)
        return jsonify(turma.__dict__), 200
    return jsonify({'message': 'Turma não encontrada'}), 404

@app.route('/api/turmas/<int:id_turma>/', methods=['DELETE'])
def delete_turma(id_turma):
    turma = next((t for t in turmas if t.id == id_turma), None)
    if turma:
        turmas.remove(turma)
        return jsonify({'message': 'Turma excluída'}), 200
    return jsonify({'message': 'Turma não encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)
