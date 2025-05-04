from flask import Blueprint, jsonify, request
from Models.model_professores import (
    Professor, listar_professores, professor_por_id,
    adicionar_professor, atualizar_professor, excluir_professor
)

professores_blueprint = Blueprint('professores', __name__)

# Rota para listar todos os professores
@professores_blueprint.route('/professores', methods=['GET'])
def get_professores():
    return jsonify(listar_professores())

# Rota para buscar um professor pelo ID
@professores_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return jsonify(professor)
    except:
        return jsonify({'erro': 'Professor não encontrado'}), 404

# Rota para criar um professor
@professores_blueprint.route('/professores', methods=['POST'])
def create_professor():
    data = request.json
    try:
        novo_professor = adicionar_professor(data)  # Função no model para criar o professor
        return jsonify(novo_professor), 201
    except KeyError as e:
        return jsonify({'erro': f"Campo obrigatório '{e.args[0]}' está faltando"}), 400

# Rota para atualizar um professor pelo ID
@professores_blueprint.route('/professores/<int:id_professor>', methods=['PUT'])
def atualizar_professor_route(id_professor):
    try:
        professor = professor_por_id(id_professor)  # Função para buscar o professor pelo ID
        data = request.json
        professor.update(data)
        return jsonify({'mensagem': f'Professor com ID {id_professor} atualizado com sucesso'}), 200
    except:
        return jsonify({'erro': 'Professor não encontrado'}), 404

# Rota para deletar um professor pelo ID
@professores_blueprint.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    try:
        excluir_professor(id_professor)
        return jsonify({'mensagem': f'Professor com ID {id_professor} deletado'}), 200
    except:
        return jsonify({'erro': 'Professor não encontrado'}), 404
