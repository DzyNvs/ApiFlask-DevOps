from itertools import count

# Gerador de IDs automáticos para professores
professor_id_gen = count(start=1)
professores = []  # Lista de professores

class ProfessorNaoEncontrado(Exception):
    pass

def listar_professores():
    return professores  # Retorna a lista completa

def professor_por_id(id_professor):
    professor = next((p for p in professores if p['id'] == id_professor), None)
    if not professor:
        raise ProfessorNaoEncontrado
    return professor

def adicionar_professor(data):
    novo_professor = {
        'id': next(professor_id_gen),
        'nome': data['nome'],
        'idade': data['idade'],
        'data_nascimento': data['data_nascimento'],
        'disciplina': data['disciplina'],
        'salario': data['salario']
    }
    professores.append(novo_professor)
    return novo_professor

def atualizar_professor(id_professor, data):
    professor = professor_por_id(id_professor)
    professor.update(data)

def excluir_professor(id_professor):
    professor = professor_por_id(id_professor)
    professores.remove(professor)
