from bd import db
from datetime import datetime, date

class AlunoNaoEncontrado(Exception):
    pass

class Aluno(db.Model):
    __tablename__ = 'alunos'  # Nome da tabela no banco de dados
    __table_args__ = {'extend_existing': True}  # Evita redefinição da tabela

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(100), nullable=False)  # Nome do aluno
    idade = db.Column(db.Integer)  # Idade do aluno
    data_nascimento = db.Column(db.String(10), nullable=False)  # Data de nascimento
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)  # Nota do primeiro semestre
    nota_segundo_semestre = db.Column(db.Float, nullable=False)  # Nota do segundo semestre
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'))  # Chave estrangeira para turmas
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))  # Chave estrangeira para professores
    
    turma = db.relationship("Turma", back_populates="alunos")

def listar_alunos():
    """Retorna todos os alunos do banco de dados."""
    return Aluno.query.all()  # Retorna todos os registros da tabela alunos

def aluno_por_id(id_aluno):
    """Retorna um aluno pelo ID."""
    aluno = Aluno.query.get(id_aluno)  # Busca o aluno pelo ID
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno

def calcular_idade(self): 
    today = date.today()
    return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))

def adicionar_aluno(data):
    """Adiciona um novo aluno ao banco de dados."""
    novo_aluno = Aluno(
        nome=data['nome'],
        idade=data.get('idade'),  # Pode ser None se não for fornecido
        data_nascimento=data['data_nascimento'],
        nota_primeiro_semestre=data['nota_primeiro_semestre'],
        nota_segundo_semestre=data['nota_segundo_semestre'],
        turma_id=data['turma_id'],
        professor_id=data['professor_id']
    )
    db.session.add(novo_aluno)  # Adiciona o novo aluno à sessão
    db.session.commit()  # Salva as alterações no banco de dados
    return novo_aluno

def atualizar_aluno(id_aluno, data):
    """Atualiza os dados de um aluno existente."""
    aluno = aluno_por_id(id_aluno)  # Busca o aluno pelo ID
    aluno.nome = data.get('nome', aluno.nome)  # Atualiza o nome se fornecido
    aluno.idade = data.get('idade', aluno.idade)  # Atualiza a idade se fornecida
    aluno.data_nascimento = data.get('data_nascimento', aluno.data_nascimento)  # Atualiza a data de nascimento se fornecida
    aluno.nota_primeiro_semestre = data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)  # Atualiza a nota do primeiro semestre se fornecida
    aluno.nota_segundo_semestre = data.get('nota_segundo_semestre', aluno.nota_segundo_semestre)  # Atualiza a nota do segundo semestre se fornecida
    aluno.turma_id = data.get('turma_id', aluno.turma_id)  # Atualiza a turma se fornecida
    aluno.professor_id = data.get('professor_id', aluno.professor_id)  # Atualiza o professor se fornecido
    db.session.commit()  # Salva as alterações no banco de dados

def excluir_aluno(id_aluno):
    """Remove um aluno do banco de dados."""
    aluno = aluno_por_id(id_aluno)  # Busca o aluno pelo ID
    db.session.delete(aluno)  # Remove o aluno da sessão
    db.session.commit()  # Salva as alterações no banco de dados