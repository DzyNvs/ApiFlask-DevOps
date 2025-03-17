import unittest
import requests

class TestAPI(unittest.TestCase):

    BASE_URL = 'http://127.0.0.1:5000'

    def setUp(self):
        # Restaura o estado inicial do servidor antes de cada teste
        r_reset = requests.post(f'{self.BASE_URL}/reseta')
        self.assertEqual(r_reset.status_code, 200)

      # --- TESTES PARA /alunos ---
    def test_001_lista_alunos_vazia(self):
        r_lista = requests.get(f'{self.BASE_URL}/Alunos')
        self.assertEqual(r_lista.status_code, 200)
        self.assertEqual(len(r_lista.json()), 0)

    def test_002_adiciona_alunos(self):
        requests.post(f'{self.BASE_URL}/Alunos', json={
            'nome': 'Fernando',
            'data_nascimento': '2000-01-01',
            'nota_primeiro_semestre': 8.0,
            'nota_segundo_semestre': 7.5,
            'turma_id': 1
        })
        requests.post(f'{self.BASE_URL}/Alunos', json={
            'nome': 'Roberto',
            'data_nascimento': '1999-05-15',
            'nota_primeiro_semestre': 7.0,
            'nota_segundo_semestre': 8.5,
            'turma_id': 2
        })
        r_lista = requests.get(f'{self.BASE_URL}/Alunos')
        lista_retornada = r_lista.json()
        self.assertTrue(any(aluno['nome'] == 'Fernando' for aluno in lista_retornada))
        self.assertTrue(any(aluno['nome'] == 'Roberto' for aluno in lista_retornada))

    def test_003_adiciona_aluno_campos_faltando(self):
        r = requests.post(f'{self.BASE_URL}/Alunos', json={'nome': 'Maria'})
        self.assertEqual(r.status_code, 400)
        # Verificar se a mensagem contém "Campo obrigatório"
        self.assertIn("Campo obrigatório", r.json().get('erro'))


    def test_004_busca_aluno_por_id(self):
    # Criar um aluno e pegar o ID do retorno
        r_post = requests.post(f'{self.BASE_URL}/Alunos', json={
        'nome': 'Mario',
        'data_nascimento': '1998-03-12',
        'nota_primeiro_semestre': 7.0,
        'nota_segundo_semestre': 8.0,
        'turma_id': 1
    })
        self.assertEqual(r_post.status_code, 201)
        aluno_id = r_post.json().get('id')  # Captura o ID retornado pelo POST

    # Buscar o aluno recém-criado pelo ID
        r = requests.get(f'{self.BASE_URL}/Alunos/{aluno_id}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get('nome'), 'Mario')

    def test_005_busca_aluno_por_id_inexistente(self):
        r = requests.get(f'{self.BASE_URL}/Alunos/999')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json().get('erro'), 'Aluno não encontrado')

    def test_006_deleta_aluno_sucesso(self):
        # Criar um aluno com todos os campos obrigatórios
        r_post = requests.post(f'{self.BASE_URL}/alunos', json={
        'nome': 'Marta',
        'data_nascimento': '1995-07-22',
        'nota_primeiro_semestre': 9.0,
        'nota_segundo_semestre': 8.5,
        'turma_id': 1
    })
        self.assertEqual(r_post.status_code, 201)  # Verifica se o aluno foi criado com sucesso
        aluno_id = r_post.json().get('id')  # Captura o ID do aluno criado

        # Deletar o aluno criado
        r = requests.delete(f'{self.BASE_URL}/alunos/{aluno_id}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get('mensagem'), f'Aluno com ID {aluno_id} deletado')
 


    def test_007_deleta_aluno_inexistente(self):
        r = requests.delete(f'{self.BASE_URL}/alunos/999')  # ID inexistente
        self.assertIn(r.status_code, [400, 404])  # Verifica se o status é apropriado
        if r.headers.get('Content-Type') == 'application/json':
            self.assertEqual(r.json().get('erro'), 'Aluno não encontrado')
        else:
            self.fail("A resposta não contém um JSON válido")


    def test_008_edita_aluno_sucesso(self):
        requests.post(f'{self.BASE_URL}/Alunos', json={
            'nome': 'Lucas',
            'data_nascimento': '2000-01-01',
            'nota_primeiro_semestre': 8.0,
            'nota_segundo_semestre': 7.5,
            'turma_id': 1
        })
        r = requests.put(f'{self.BASE_URL}/Alunos/1', json={'nome': 'Lucas Mendes'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get('mensagem'), 'Aluno com ID 1 atualizado com sucesso')

    def test_009_edita_aluno_inexistente(self):
        r = requests.put(f'{self.BASE_URL}/Alunos/999', json={'nome': 'Atualizado'})
        self.assertIn(r.status_code, [400, 404])
        self.assertEqual(r.json().get('erro'), 'Aluno não encontrado')

    def test_010_reseta_funciona(self):
        requests.post(f'{self.BASE_URL}/Alunos', json={
            'nome': 'Cicero',
            'data_nascimento': '1997-02-02',
            'nota_primeiro_semestre': 6.5,
            'nota_segundo_semestre': 7.0,
            'turma_id': 2
        })
        r_reset = requests.post(f'{self.BASE_URL}/reseta')
        self.assertEqual(r_reset.status_code, 200)
        r_lista = requests.get(f'{self.BASE_URL}/Alunos')
        self.assertEqual(len(r_lista.json()), 0)

    # --- TESTES PARA /professores ---
    def test_100_professores_retorna_lista(self):
        r = requests.get(f'{self.BASE_URL}/Professores')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(type(r.json()), list)

    def test_101_adiciona_professores(self):
        requests.post(f'{self.BASE_URL}/Professores', json={
        'nome': 'Fernando',
        'idade': 40,
        'data_nascimento': '1982-05-15',
        'disciplina': 'Matemática',
        'salario': 3000
    })
        requests.post(f'{self.BASE_URL}/Professores', json={
        'nome': 'Roberto',
        'idade': 45,
        'data_nascimento': '1977-04-10',
        'disciplina': 'História',
        'salario': 3500
    })
        r_lista = requests.get(f'{self.BASE_URL}/Professores')
        lista_retornada = r_lista.json()
        self.assertTrue(any(professor['nome'] == 'Fernando' for professor in lista_retornada))
        self.assertTrue(any(professor['nome'] == 'Roberto' for professor in lista_retornada))

    def test_102_professores_por_id(self):
        requests.post(f'{self.BASE_URL}/Professores', json={
        'nome': 'Mario',
        'idade': 50,
        'data_nascimento': '1973-03-12',
        'disciplina': 'Geografia',
        'salario': 4000
    })
        r = requests.get(f'{self.BASE_URL}/Professores/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get('nome'), 'Mario')

    def test_103_professores_reseta(self):
        requests.post(f'{self.BASE_URL}/Professores', json={
        'nome': 'Cicero',
        'idade': 35,
        'data_nascimento': '1988-02-02',
        'disciplina': 'Física',
        'salario': 3200
    })
        r_reset = requests.post(f'{self.BASE_URL}/reseta')
        self.assertEqual(r_reset.status_code, 200)
        r_lista = requests.get(f'{self.BASE_URL}/Professores')
        self.assertEqual(len(r_lista.json()), 0)

    def test_104_deleta_professor(self):
        requests.post(f'{self.BASE_URL}/Professores', json={
        'nome': 'Lucas',
        'idade': 38,
        'data_nascimento': '1985-06-15',
        'disciplina': 'Química',
        'salario': 3000
    })
        r = requests.delete(f'{self.BASE_URL}/Professores/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get('mensagem'), 'Professor com ID 1 deletado')

    def test_105_edita_professor(self):
        requests.post(f'{self.BASE_URL}/Professores', json={
        'nome': 'Lucas',
        'idade': 38,
        'data_nascimento': '1985-06-15',
        'disciplina': 'Química',
        'salario': 3000
    })
        r = requests.put(f'{self.BASE_URL}/Professores/1', json={'nome': 'Lucas Mendes'})
        self.assertEqual(r.status_code, 200)
        r_apos = requests.get(f'{self.BASE_URL}/Professores/1')
        self.assertEqual(r_apos.json().get('nome'), 'Lucas Mendes')

    def test_106_professor_id_inexistente(self):
        r = requests.get(f'{self.BASE_URL}/Professores/999')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json().get('erro'), 'Professor não encontrado')

    def test_107_criar_professor_com_id_existente(self):
        requests.post(f'{self.BASE_URL}/Professores', json={
        'nome': 'Bond',
        'idade': 40,
        'data_nascimento': '1980-11-22',
        'disciplina': 'Espionagem',
        'salario': 5000
    })
        r = requests.post(f'{self.BASE_URL}/Professores', json={
        'nome': 'James',
        'idade': 45,
        'data_nascimento': '1975-05-14',
        'disciplina': 'Ação',
        'salario': 5500,
        'id': 1
    })
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get('erro'), 'ID já utilizada')

    def test_108_post_professor_sem_nome(self):
        r = requests.post(f'{self.BASE_URL}/Professores', json={
        'idade': 30,
        'data_nascimento': '1993-01-01',
        'disciplina': 'Biologia',
        'salario': 2800
    })
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get('erro'), 'Professor sem nome')


    # --- Testes Turma --- #
    def test_200_lista_turmas_vazia(self):
        r_lista = requests.get(f'{self.BASE_URL}/Turmas')
        self.assertEqual(r_lista.status_code, 200)
        self.assertEqual(len(r_lista.json()), 0)

    def test_201_adiciona_turmas(self):
        requests.post(f'{self.BASE_URL}/Turmas', json={
        'nome': 'Turma A',
        'turno': 'Manhã',
        'professor_id': 1
    })
        requests.post(f'{self.BASE_URL}/Turmas', json={
        'nome': 'Turma B',
        'turno': 'Tarde',
        'professor_id': 2
    })
        r_lista = requests.get(f'{self.BASE_URL}/Turmas')
        lista_retornada = r_lista.json()
        self.assertTrue(any(turma['nome'] == 'Turma A' for turma in lista_retornada))
        self.assertTrue(any(turma['nome'] == 'Turma B' for turma in lista_retornada))

    def test_202_turmas_por_id(self):
        requests.post(f'{self.BASE_URL}/Turmas', json={
        'nome': 'Turma C',
        'turno': 'Noite',
        'professor_id': 3
    })
        r = requests.get(f'{self.BASE_URL}/Turmas/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get('nome'), 'Turma C')

    def test_203_turmas_reseta(self):
        requests.post(f'{self.BASE_URL}/Turmas', json={
        'nome': 'Turma D',
        'turno': 'Manhã',
        'professor_id': 1
    })
        r_reset = requests.post(f'{self.BASE_URL}/reseta')
        self.assertEqual(r_reset.status_code, 200)
        r_lista = requests.get(f'{self.BASE_URL}/Turmas')
        self.assertEqual(len(r_lista.json()), 0)

    def test_204_deleta_turma(self):
        requests.post(f'{self.BASE_URL}/Turmas', json={
        'nome': 'Turma E',
        'turno': 'Tarde',
        'professor_id': 2
    })
        r = requests.delete(f'{self.BASE_URL}/Turmas/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get('mensagem'), 'Turma com ID 1 deletado')

    def test_205_edita_turma(self):
        requests.post(f'{self.BASE_URL}/Turmas', json={
        'nome': 'Turma F',
        'turno': 'Noite',
        'professor_id': 3
    })
        r = requests.put(f'{self.BASE_URL}/Turmas/1', json={'nome': 'Turma F Atualizada'})
        self.assertEqual(r.status_code, 200)
        r_apos = requests.get(f'{self.BASE_URL}/Turmas/1')
        self.assertEqual(r_apos.json().get('nome'), 'Turma F Atualizada')

    def test_206_turma_id_inexistente(self):
        r = requests.get(f'{self.BASE_URL}/Turmas/999')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json().get('erro'), 'Turma não encontrada')

    def test_207_criar_turma_sem_professor_id(self):
        r = requests.post(f'{self.BASE_URL}/Turmas', json={
        'nome': 'Turma G',
        'turno': 'Manhã'
    })
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get('erro'), 'Campos obrigatórios faltando')

    def test_208_turmas_nao_confundir_com_professores(self):
        requests.post(f'{self.BASE_URL}/Professores', json={
        'nome': 'Fernando',
        'idade': 40,
        'data_nascimento': '1982-05-15',
        'disciplina': 'Matemática',
        'salario': 3000
    })
        requests.post(f'{self.BASE_URL}/Turmas', json={
        'nome': 'Turma H',
        'turno': 'Tarde',
        'professor_id': 1
    })
        r_lista_turmas = requests.get(f'{self.BASE_URL}/Turmas')
        self.assertEqual(len(r_lista_turmas.json()), 1)
        r_lista_professores = requests.get(f'{self.BASE_URL}/Professores')
        self.assertEqual(len(r_lista_professores.json()), 1)


if __name__ == '__main__':
    unittest.main()
