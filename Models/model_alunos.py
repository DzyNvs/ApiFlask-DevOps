from datetime import datetime
from bd import db  # Importe o objeto db corretamente

# Exceção personalizada para aluno não encontrado
class AlunoNaoEncontrado(Exception):
    pass

class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)
    nota_segundo_semestre = db.Column(db.Float, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'))

    turma_relacao = db.relationship("Turma", back_populates="alunos")

    @property
    def idade(self):
        """Calcula a idade com base na data de nascimento, validando o formato."""
        try:
            data_nasc = datetime.strptime(self.data_nascimento, "%Y-%m-%d")
            hoje = datetime.today()
            return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        except ValueError:
            return None  # Retorna `None` se a data for inválida

    @property
    def media_final(self):
        """Calcula a média final do aluno."""
        return (self.nota_primeiro_semestre + self.nota_segundo_semestre) / 2

    def to_dict(self):
        """Converte um objeto Aluno para um dicionário JSON serializável"""
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,  # Agora validado
            "data_nascimento": self.data_nascimento,
            "nota_primeiro_semestre": self.nota_primeiro_semestre,
            "nota_segundo_semestre": self.nota_segundo_semestre,
            "media_final": self.media_final,
            "turma_id": self.turma_id,
        }

def listar_alunos():
    """Retorna todos os alunos do banco de dados."""
    return [aluno.to_dict() for aluno in Aluno.query.all()]

def aluno_por_id(id_aluno):
    """Retorna um aluno pelo ID."""
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado(f"Aluno com ID {id_aluno} não encontrado.")
    return aluno.to_dict()

def adicionar_aluno(data):
    """Adiciona um novo aluno ao banco de dados."""
    novo_aluno = Aluno(
        nome=data['nome'],
        data_nascimento=data['data_nascimento'],
        nota_primeiro_semestre=data['nota_primeiro_semestre'],
        nota_segundo_semestre=data['nota_segundo_semestre'],
        turma_id=data['turma_id'],
    )
    db.session.add(novo_aluno)
    db.session.commit()
    return novo_aluno.to_dict()

def atualizar_aluno(id_aluno, data):
    """Atualiza os dados de um aluno existente."""
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado(f"Aluno com ID {id_aluno} não encontrado.")

    aluno.nome = data.get('nome', aluno.nome)
    aluno.data_nascimento = data.get('data_nascimento', aluno.data_nascimento)
    aluno.nota_primeiro_semestre = data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
    aluno.nota_segundo_semestre = data.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
    aluno.turma_id = data.get('turma_id', aluno.turma_id)
    
    db.session.commit()
    return aluno.to_dict()

def excluir_aluno(id_aluno):
    """Remove um aluno do banco de dados."""
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado(f"Aluno com ID {id_aluno} não encontrado.")
    
    db.session.delete(aluno)
    db.session.commit()
    return {"mensagem": f"Aluno com ID {id_aluno} foi removido com sucesso."}
