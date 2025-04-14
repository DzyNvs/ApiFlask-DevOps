from itertools import count

# Gerador de IDs automáticos para alunos
aluno_id_gen = count(start=1)
alunos = []  # Lista de alunos

class AlunoNaoEncontrado(Exception):
    pass

def listar_alunos():
    return alunos  # Retorna a lista completa

def aluno_por_id(id_aluno):
    aluno = next((a for a in alunos if a['id'] == id_aluno), None)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno

def adicionar_aluno(data):
    if not all(k in data for k in ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id', 'professor_id']):
        raise KeyError("Campo obrigatório está faltando")

    novo_aluno = {
        'id': next(aluno_id_gen),
        'nome': data['nome'],
        'data_nascimento': data['data_nascimento'],
        'nota_primeiro_semestre': data['nota_primeiro_semestre'],
        'nota_segundo_semestre': data['nota_segundo_semestre'],
        'turma_id': data['turma_id'],
        'professor_id': data['professor_id']
    }
    alunos.append(novo_aluno)
    return novo_aluno


def atualizar_aluno(id_aluno, data):
    aluno = aluno_por_id(id_aluno)
    aluno.update(data)

def excluir_aluno(id_aluno):
    aluno = aluno_por_id(id_aluno)
    alunos.remove(aluno)
