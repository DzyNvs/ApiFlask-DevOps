from flask import Blueprint, jsonify, request
from Models.model_turmas import (
    TurmaNaoEncontrada, listar_turmas, turma_por_id,
    adicionar_turma, atualizar_turma, excluir_turma, turmas
)

turmas_blueprint = Blueprint('turmas', __name__)

# Rota para listar todas as turmas
@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    return jsonify(listar_turmas())

# Rota para buscar uma turma pelo ID
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)  
        return jsonify(turma), 200  
    except TurmaNaoEncontrada:
        return jsonify({'erro': 'Turma não encontrada'}), 404  

# Rota para criar uma turma
@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    data = request.json
    try:
        nova_turma = adicionar_turma(data)  # Função no model para adicionar a turma
        return jsonify(nova_turma), 201
    except KeyError:
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400




# Rota para atualizar uma turma pelo ID
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
    try:
        # Tenta buscar a turma pelo ID
        turma = turma_por_id(id_turma)
        data = request.json  # Obtém os dados enviados na requisição
        turma.update(data)  # Atualiza os campos da turma
        return jsonify({'mensagem': f'Turma com ID {id_turma} atualizada com sucesso'}), 200
    except TurmaNaoEncontrada:
        return jsonify({'erro': 'Turma não encontrada'}), 404  # Retorna erro caso não encontre a turma
    except KeyError as e:
        return jsonify({'erro': f"Campo obrigatório '{e.args[0]}' está faltando"}), 400


# Rota para deletar uma turma pelo ID
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    try:
        # Verifica se a turma existe
        turma = turma_por_id(id_turma)
        # Remove a turma da lista
        excluir_turma(id_turma)
        return jsonify({'mensagem': f'Turma com ID {id_turma} deletada'}), 200
    except TurmaNaoEncontrada:
        return jsonify({'erro': 'Turma não encontrada'}), 404


@turmas_blueprint.route('/reseta_turmas', methods=['POST'])
def reset_turmas():
    turmas.clear()  # Limpa a lista de turmas
    return jsonify({'mensagem': 'Lista de turmas resetada com sucesso'}), 200

