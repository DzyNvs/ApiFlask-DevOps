from bd import db
from datetime import datetime

# Exceção personalizada para professor não encontrado
class ProfessorNaoEncontrado(Exception):
    pass

class Professor(db.Model):
    __tablename__ = 'professores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    disciplina = db.Column(db.String(100), nullable=True)

    def calcular_idade(self):
        """Calcula a idade com base na data de nascimento, validando o formato."""
        try:
            data_nasc = datetime.strptime(self.data_nascimento, "%Y-%m-%d")
            hoje = datetime.today()
            return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        except ValueError:
            return None 

    def to_dict(self):
        """Converte um objeto Professor para um dicionário JSON serializável"""
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.calcular_idade(),  # Agora chamamos explicitamente
            "data_nascimento": self.data_nascimento,
            "disciplina": self.disciplina,
        }


def listar_professores():
    """Retorna todos os professores do banco de dados."""
    return [professor.to_dict() for professor in Professor.query.all()]

def professor_por_id(id_professor):
    """Retorna um professor pelo ID."""
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado(f"Professor com ID {id_professor} não encontrado.")
    return professor.to_dict()

def adicionar_professor(data):
    """Adiciona um novo professor ao banco de dados."""
    novo_professor = Professor(
        nome=data['nome'],
        data_nascimento=data['data_nascimento'],
        disciplina=data.get('disciplina')
    )
    db.session.add(novo_professor)
    db.session.commit()
    return novo_professor.to_dict()

def atualizar_professor(id_professor, data):
    """Atualiza os dados de um professor existente e retorna os dados atualizados"""
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado(f"Professor com ID {id_professor} não encontrado.")

    professor.nome = data.get('nome', professor.nome)
    professor.data_nascimento = data.get('data_nascimento', professor.data_nascimento)
    professor.disciplina = data.get('disciplina', professor.disciplina)

    db.session.commit()  # Garante que a atualização é salva no banco

    return professor.to_dict()  # Retorna os dados atualizados corretamente

def excluir_professor(id_professor):
    """Remove um professor do banco de dados."""
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado(f"Professor com ID {id_professor} não encontrado.")

    db.session.delete(professor)
    db.session.commit()
    return {"mensagem": f"Professor com ID {id_professor} foi removido com sucesso."}
