from itertools import count

# Geradores automáticos de ID
aluno_id_gen = count(start=1)
professor_id_gen = count(start=1)
turma_id_gen = count(start=1)

# Bases de dados
Alunos = []
Professores = []
Turmas = []

# Funções para adicionar registros
def add_aluno(nome, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre, turma_id):
    novo_aluno = {
        'id': next(aluno_id_gen),
        'nome': nome,
        'data_nascimento': data_nascimento,
        'nota_primeiro_semestre': nota_primeiro_semestre,
        'nota_segundo_semestre': nota_segundo_semestre,
        'turma_id': turma_id
    }
    Alunos.append(novo_aluno)
    return novo_aluno

def add_professor(nome, idade, data_nascimento, disciplina, salario):
    novo_professor = {
        'id': next(professor_id_gen),
        'nome': nome,
        'idade': idade,
        'data_nascimento': data_nascimento,
        'disciplina': disciplina,
        'salario': salario
    }
    Professores.append(novo_professor)
    return novo_professor

def add_turma(nome, turno, professor_id):
    nova_turma = {
        'id': next(turma_id_gen),
        'nome': nome,
        'turno': turno,
        'professor_id': professor_id
    }
    Turmas.append(nova_turma)
    return nova_turma