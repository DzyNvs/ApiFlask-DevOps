import unittest
from Models.model_alunos import Aluno
from Models.model_professores import Professor
from Models.model_turmas import Turma
from app import app, db


class TestApp(unittest.TestCase):
    def setUp(self):
        """Configura um banco de dados de teste."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usa um banco em memória para testes mais rápidos
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Limpa o banco de dados após cada teste."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Testes internos de Aluno
    def test_criar_aluno_no_banco(self):
        with app.app_context():
            aluno = Aluno(nome='João', data_nascimento='2002-05-20', nota_primeiro_semestre=8.5, nota_segundo_semestre=9.0, turma_id=None)
            db.session.add(aluno)
            db.session.commit()
            self.assertEqual(Aluno.query.count(), 1)
            self.assertEqual(aluno.nome, 'João')

    def test_atualizar_aluno_no_banco(self):
        with app.app_context():
            aluno = Aluno(nome='Maria', data_nascimento='2001-03-15', nota_primeiro_semestre=7.0, nota_segundo_semestre=8.0, turma_id=None)
            db.session.add(aluno)
            db.session.commit()
            aluno.nome = 'Maria Silva'
            db.session.commit()
            updated_aluno = Aluno.query.first()
            self.assertEqual(updated_aluno.nome, 'Maria Silva')

    def test_deletar_aluno_no_banco(self):
        with app.app_context():
            aluno = Aluno(nome='Carlos', data_nascimento='2000-08-25', nota_primeiro_semestre=7.5, nota_segundo_semestre=6.5, turma_id=None)
            db.session.add(aluno)
            db.session.commit()
            db.session.delete(aluno)
            db.session.commit()
            self.assertEqual(Aluno.query.count(), 0)

    # Testes internos de Professor
    def test_criar_professor_no_banco(self):
        with app.app_context():
            professor = Professor(nome='Paulo', data_nascimento='1980-07-12', disciplina='Matemática')
            db.session.add(professor)
            db.session.commit()
            self.assertEqual(Professor.query.count(), 1)
            self.assertEqual(professor.nome, 'Paulo')

    def test_atualizar_professor_no_banco(self):
        with app.app_context():
            professor = Professor(nome='Fernanda', data_nascimento='1985-06-22', disciplina='História')
            db.session.add(professor)
            db.session.commit()
            professor.nome = 'Fernanda Silva'
            db.session.commit()
            updated_professor = Professor.query.first()
            self.assertEqual(updated_professor.nome, 'Fernanda Silva')

    def test_deletar_professor_no_banco(self):
        with app.app_context():
            professor = Professor(nome='Bianca', data_nascimento='1992-09-10', disciplina='Química')
            db.session.add(professor)
            db.session.commit()
            db.session.delete(professor)
            db.session.commit()
            self.assertEqual(Professor.query.count(), 0)

    # Testes internos de Turma
    def test_criar_turma_no_banco(self):
        with app.app_context():
            professor = Professor(nome='Rita', data_nascimento='1975-01-05', disciplina='Física')
            db.session.add(professor)
            db.session.commit()
            turma = Turma(nome='1A', turno='Matutino', professor_id=professor.id)
            db.session.add(turma)
            db.session.commit()
            self.assertEqual(Turma.query.count(), 1)
            self.assertEqual(turma.nome, '1A')

    def test_atualizar_turma_no_banco(self):
        with app.app_context():
            professor = Professor(nome='Henrique', data_nascimento='1988-04-30', disciplina='Biologia')
            db.session.add(professor)
            db.session.commit()
            turma = Turma(nome='2B', turno='Vespertino', professor_id=professor.id)
            db.session.add(turma)
            db.session.commit()
            turma.nome = '2B Avançada'
            db.session.commit()
            updated_turma = Turma.query.first()
            self.assertEqual(updated_turma.nome, '2B Avançada')

    def test_deletar_turma_no_banco(self):
        with app.app_context():
            professor = Professor(nome='Joana', data_nascimento='1980-12-15', disciplina='Educação Física')
            db.session.add(professor)
            db.session.commit()
            turma = Turma(nome='4D', turno='Noturno', professor_id=professor.id)
            db.session.add(turma)
            db.session.commit()
            db.session.delete(turma)
            db.session.commit()
            self.assertEqual(Turma.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
