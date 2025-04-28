from bd import db

class TurmaNaoEncontrada(Exception):
    pass

class Turma(db.Model):
    __tablename__ = 'turmas'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(100), nullable=False)  # Nome da turma
    turno = db.Column(db.String(50), nullable=False)  # Turno da turma
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))  # Chave estrangeira para professores

    # Relacionamentos
    alunos = db.relationship('Aluno', backref='turma', lazy=True)  # Relacionamento com Aluno

def listar_turmas():
    """Retorna todas as turmas do banco de dados."""
    return Turma.query.all()  # Retorna todos os registros da tabela turmas

def turma_por_id(id_turma):
    """Retorna uma turma pelo ID."""
    turma = Turma.query.get(id_turma)  # Busca a turma pelo ID
    if not turma:
        raise TurmaNaoEncontrada
    return turma

def adicionar_turma(data):
    """Adiciona uma nova turma ao banco de dados."""
    nova_turma = Turma(
        nome=data['nome'],
        turno=data['turno'],
        professor_id=data['professor_id']
    )
    db.session.add(nova_turma)  # Adiciona a nova turma à sessão
    db.session.commit()  # Salva as alterações no banco de dados
    return nova_turma

def atualizar_turma(id_turma, data):
    """Atualiza os dados de uma turma existente."""
    turma = turma_por_id(id_turma)  # Busca a turma pelo ID
    turma.nome = data.get('nome', turma.nome)  # Atualiza o nome se fornecido
    turma.turno = data.get('turno', turma.turno)  # Atualiza o turno se fornecido
    turma.professor_id = data.get('professor_id', turma.professor_id)  # Atualiza o professor se fornecido
    db.session.commit()  # Salva as alterações no banco de dados

def excluir_turma(id_turma):
    """Remove uma turma do banco de dados."""
    turma = turma_por_id(id_turma)  # Busca a turma pelo ID
    db.session.delete(turma)  # Remove a turma da sessão
    db.session.commit()  # Salva as alterações no banco de dados