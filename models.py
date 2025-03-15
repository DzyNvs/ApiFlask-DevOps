class Professor:
    def __init__(self, nome, idade, materia, observacoes):
        self.id = None
        self.nome = nome
        self.idade = idade 
        self.materia = materia
        self.observacoes = observacoes 
        

class Turma:
    def __init__(self, descricao, professor_id, ativo):
        self.id = None
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo
        

class Aluno:
    def __init__(self, nome, idade, turma_id, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre, media_final):
        self.id = None
        self.nome = nome
        self.idade = idade
        self.turma_id = turma_id
        self.data_nascimento = data_nascimento
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.media_final = media_final
    
    def calcular_media(self):
        return (self.nota_primeiro_semestre + self.nota_segundo_semestre) / 2 if self.nota_primeiro_semestre is not None and self.nota_segundo_semestre is not None else None