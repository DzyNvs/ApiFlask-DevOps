from flask import Blueprint, jsonify, request
from Models.model_turmas import (
    TurmaNaoEncontrada, listar_turmas, turma_por_id,
    adicionar_turma, atualizar_turma, excluir_turma
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
        return jsonify(turma_por_id(id_turma))
    except TurmaNaoEncontrada:
        return jsonify({'erro': 'Turma não encontrada'}), 404

# Rota para criar uma turma
@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    data = request.json
    try:
        nova_turma = adicionar_turma(data)
        return jsonify(nova_turma), 201
    except KeyError as e:
        return jsonify({'erro': f"Campo obrigatório '{e.args[0]}' está faltando"}), 400

# Rota para atualizar uma turma pelo ID
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['PUT'])
def atualizar_turma_route(id_turma):
    try:
        data = request.json
        turma_atualizada = atualizar_turma(id_turma, data)
        return jsonify(turma_atualizada), 200
    except TurmaNaoEncontrada:
        return jsonify({'erro': 'Turma não encontrada'}), 404

# Rota para deletar uma turma pelo ID
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    try:
        return jsonify(excluir_turma(id_turma)), 200
    except TurmaNaoEncontrada:
        return jsonify({'erro': 'Turma não encontrada'}), 404
