from itertools import count

# Gerador de IDs automáticos para turmas
turma_id_gen = count(start=1)
turmas = []  # Lista de turmas

class TurmaNaoEncontrada(Exception):
    pass

def listar_turmas():
    return turmas  # Retorna a lista completa

def turma_por_id(id_turma):
    turma = next((t for t in turmas if t['id'] == id_turma), None)
    if not turma:
        raise TurmaNaoEncontrada
    return turma

def adicionar_turma(data):
    nova_turma = {
        'id': next(turma_id_gen),
        'nome': data['nome'],
        'turno': data['turno'],
        'professor_id': data['professor_id']
    }
    turmas.append(nova_turma)
    return nova_turma

def atualizar_turma(id_turma, data):
    turma = turma_por_id(id_turma)
    turma.update(data)

def excluir_turma(id_turma):
    turma = turma_por_id(id_turma)
    turmas.remove(turma)
