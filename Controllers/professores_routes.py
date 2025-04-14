from flask import Blueprint, jsonify, request
from Models.model_professores import (
    ProfessorNaoEncontrado, listar_professores, professor_por_id,
    adicionar_professor, atualizar_professor, excluir_professor, professores
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
    except ProfessorNaoEncontrado:
        return jsonify({'erro': 'Professor não encontrado'}), 404

# Rota para criar um professor
@professores_blueprint.route('/professores', methods=['POST'])
def create_professor():
    try:
        data = request.json

        # Validação de ID duplicado
        if 'id' in data and any(professor['id'] == data['id'] for professor in professores):
            return jsonify({'erro': 'ID já utilizado'}), 400  # Retorna erro 400 se o ID já existir

        # Caso não haja duplicidade, cria o professor
        novo_professor = adicionar_professor(data)
        return jsonify(novo_professor), 201  # Retorna sucesso com status 201
    except KeyError as e:
        return jsonify({'erro': f"Campo obrigatório '{e.args[0]}' está faltando"}), 400  # Valida campos obrigatórios






# Rota para atualizar um professor pelo ID
@professores_blueprint.route('/professores/<int:id_professor>', methods=['PUT'])
def update_professor(id_professor):
    try:
        data = request.json
        professor = professor_por_id(id_professor)  # Busca o professor por ID
        professor.update(data)  # Atualiza os campos do professor
        return jsonify({'mensagem': f'Professor com ID {id_professor} atualizado com sucesso'}), 200
    except ProfessorNaoEncontrado:
        return jsonify({'erro': 'Professor não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
 


# Rota para deletar um professor pelo ID
@professores_blueprint.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    try:
        excluir_professor(id_professor)
        return jsonify({'mensagem': f'Professor com ID {id_professor} deletado'}), 200
    except ProfessorNaoEncontrado:
        return jsonify({'erro': 'Professor não encontrado'}), 404

@professores_blueprint.route('/reseta_professores', methods=['POST'])
def reset_professores():
    professores.clear()  
    return jsonify({'mensagem': 'Lista de professores resetada com sucesso'}), 200

