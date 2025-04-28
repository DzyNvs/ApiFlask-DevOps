from bd import db

class ProfessorNaoEncontrado(Exception):
    pass

class Professor(db.Model):
    __tablename__ = 'professores'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(100), nullable=False)  # Nome do professor
    idade = db.Column(db.Integer)  # Idade do professor
    data_nascimento = db.Column(db.String(10), nullable=False)  # Data de nascimento
    disciplina = db.Column(db.String(100), nullable=False)  # Disciplina que leciona
    salario = db.Column(db.Float, nullable=False)  # Salário do professor

def listar_professores():
    """Retorna todos os professores do banco de dados."""
    return Professor.query.all()  # Retorna todos os registros da tabela professores

def professor_por_id(id_professor):
    """Retorna um professor pelo ID."""
    professor = Professor.query.get(id_professor)  # Busca o professor pelo ID
    if not professor:
        raise ProfessorNaoEncontrado
    return professor

def adicionar_professor(data):
    """Adiciona um novo professor ao banco de dados."""
    novo_professor = Professor(
        nome=data['nome'],
        idade=data.get('idade'),  # Pode ser None se não for fornecido
        data_nascimento=data['data_nascimento'],
        disciplina=data['disciplina'],
        salario=data['salario']
    )
    db.session.add(novo_professor)  # Adiciona o novo professor à sessão
    db.session.commit()  # Salva as alterações no banco de dados
    return novo_professor

def atualizar_professor(id_professor, data):
    """Atualiza os dados de um professor existente."""
    professor = professor_por_id(id_professor)  # Busca o professor pelo ID
    professor.nome = data.get('nome', professor.nome)  # Atualiza o nome se fornecido
    professor.idade = data.get('idade', professor.idade)  # Atualiza a idade se fornecida
    professor.data_nascimento = data.get('data_nascimento', professor.data_nascimento)  # Atualiza a data de nascimento se fornecida
    professor.disciplina = data.get('disciplina', professor.disciplina)  # Atualiza a disciplina se fornecida
    professor.salario = data.get('salario', professor.salario)  # Atualiza o salário se fornecido
    db.session.commit()  # Salva as alterações no banco de dados

def excluir_professor(id_professor):
    """Remove um professor do banco de dados."""
    professor = professor_por_id(id_professor)  # Busca o professor pelo ID
    db.session.delete(professor)  # Remove o professor da sessão
    db.session.commit()  # Salva as alterações no banco de dados