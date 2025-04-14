from flask import Blueprint, jsonify, request
from Models.model_alunos import (
    AlunoNaoEncontrado, listar_alunos, aluno_por_id,
    adicionar_aluno, atualizar_aluno, excluir_aluno, alunos
)

alunos_blueprint = Blueprint('alunos', __name__)

# Rota para listar todos os alunos
@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(listar_alunos())

# Rota para buscar um aluno pelo ID
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return jsonify(aluno)
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'Aluno não encontrado'}), 404

# Rota para criar um aluno
@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.json
    try:
        novo_aluno = adicionar_aluno(data)  # Função no model para criar o aluno
        return jsonify(novo_aluno), 201
    except KeyError as e:
        return jsonify({'erro': f"Campo obrigatório '{e.args[0]}' está faltando"}), 400



# Rota para atualizar um aluno pelo ID
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)  # Função para buscar o aluno pelo ID
        data = request.json
        aluno.update(data)
        return jsonify({'mensagem': f'Aluno com ID {id_aluno} atualizado com sucesso'}), 200
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'Aluno não encontrado'}), 404  # Retorno em JSON


# Rota para deletar um aluno pelo ID
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return jsonify({'mensagem': f'Aluno com ID {id_aluno} deletado'}), 200
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'Aluno não encontrado'}), 404

@alunos_blueprint.route('/reseta_alunos', methods=['POST'])
def reset_alunos():
    alunos.clear()
    return jsonify({'mensagem': 'Lista de alunos resetada com sucesso'}), 200

