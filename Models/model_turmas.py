from bd import db
from Models.model_alunos import Aluno  # Importação correta para relacionamento

class TurmaNaoEncontrada(Exception):
    pass

class Turma(db.Model):
    __tablename__ = 'turmas'
    __table_args__ = {'extend_existing': True}  # Evita redefinição da tabela

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    turno = db.Column(db.String(50), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))

    # Relacionamento com Alunos
    alunos = db.relationship('Aluno', backref='turma', lazy=True)

def listar_turmas():
    """Retorna todas as turmas do banco de dados."""
    return [turma.__dict__ for turma in Turma.query.all()]  # Corrigido para retorno JSON serializável

def turma_por_id(id_turma):
    """Retorna uma turma pelo ID."""
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    return turma.__dict__  # Retorno JSON serializável

def adicionar_turma(data):
    """Adiciona uma nova turma ao banco de dados."""
    nova_turma = Turma(
        nome=data['nome'],
        turno=data['turno'],
        professor_id=data['professor_id']
    )
    db.session.add(nova_turma)
    db.session.commit()
    return nova_turma.__dict__

def atualizar_turma(id_turma, data):
    """Atualiza os dados de uma turma existente."""
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada

    turma.nome = data.get('nome', turma.nome)
    turma.turno = data.get('turno', turma.turno)
    turma.professor_id = data.get('professor_id', turma.professor_id)
    db.session.commit()
    return turma.__dict__

def excluir_turma(id_turma):
    """Remove uma turma do banco de dados."""
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    db.session.delete(turma)
    db.session.commit()
    return {'mensagem': f'Turma com ID {id_turma} deletada'}
