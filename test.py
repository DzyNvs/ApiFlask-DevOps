
import unittest
import requests

class TestAPI(unittest.TestCase):

    BASE_URL = 'http://127.0.0.1:5000'

    def setUp(self):
        # Restaura o estado inicial do servidor antes de cada teste
        r_reset_alunos = requests.post(f'{self.BASE_URL}/reseta_alunos')
        self.assertEqual(r_reset_alunos.status_code, 200)

        r_reset_professores = requests.post(f'{self.BASE_URL}/reseta_professores')
        self.assertEqual(r_reset_professores.status_code, 200)

        r_reset_turmas = requests.post(f'{self.BASE_URL}/reseta_turmas')
        self.assertEqual(r_reset_turmas.status_code, 200)

        # Cria dois professores
        r_prof1 = requests.post(f'{self.BASE_URL}/professores', json={
            'nome': 'Prof. Ana',
            'idade': 40,
            'data_nascimento': '1984-03-20',
            'disciplina': 'Matemática',
            'salario': 5000
        })
        self.assertEqual(r_prof1.status_code, 201)
        self.professor_id_1 = r_prof1.json().get('id')

        r_prof2 = requests.post(f'{self.BASE_URL}/professores', json={
            'nome': 'Prof. Roberto',
            'idade': 45,
            'data_nascimento': '1977-04-10',
            'disciplina': 'História',
            'salario': 3500
        })
        self.assertEqual(r_prof2.status_code, 201)
        self.professor_id_2 = r_prof2.json().get('id')



      # --- TESTES PARA /alunos ---
    def test_001_lista_alunos_vazia(self):
        r_lista = requests.get(f'{self.BASE_URL}/alunos')
        self.assertEqual(r_lista.status_code, 200)
        self.assertEqual(len(r_lista.json()), 0)

    def test_002_adiciona_alunos(self):
    # 1. Cria um professor
        r_prof = requests.post(f'{self.BASE_URL}/professores', json={
            'nome': 'Prof. Ana',
            'idade': 40,
            'data_nascimento': '1984-03-20',
            'disciplina': 'Matemática',
            'salario': 5000
        })
        professor = r_prof.json()
        professor_id = professor['id']

    
        # 2. Cria duas turmas usando esse professor
        r_turma1 = requests.post(f'{self.BASE_URL}/turmas', json={
            'nome': 'Turma A',
            'turno': 'Manhã',
            'professor_id': professor_id
        })
        turma1 = r_turma1.json()
    
        r_turma2 = requests.post(f'{self.BASE_URL}/turmas', json={
            'nome': 'Turma B',
            'turno': 'Tarde',
            'professor_id': professor_id
        })
        turma2 = r_turma2.json()
    
        # 3. Adiciona os alunos
        requests.post(f'{self.BASE_URL}/alunos', json={
            'nome': 'Fernando',
            'data_nascimento': '2000-01-01',
            'nota_primeiro_semestre': 8.0,
            'nota_segundo_semestre': 7.5,
            'turma_id': turma1['id'],
            'professor_id': professor_id
        })
    
        requests.post(f'{self.BASE_URL}/alunos', json={
            'nome': 'Roberto',
            'data_nascimento': '1999-05-15',
            'nota_primeiro_semestre': 7.0,
            'nota_segundo_semestre': 8.5,
            'turma_id': turma2['id'],
            'professor_id': professor_id
        })

        # 4. Lista e valida
        r_lista = requests.get(f'{self.BASE_URL}/alunos')
        lista_retornada = r_lista.json()

        self.assertTrue(any(aluno['nome'] == 'Fernando' for aluno in lista_retornada))
        self.assertTrue(any(aluno['nome'] == 'Roberto' for aluno in lista_retornada))

    def test_003_adiciona_aluno_campos_faltando(self):
        r = requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'Maria'})
        self.assertEqual(r.status_code, 400)
        self.assertIn("Campo obrigatório", r.json().get('erro'))  # Verifica parte do texto na mensagem de erro
        

    def test_005_busca_aluno_por_id_inexistente(self):
        r = requests.get(f'{self.BASE_URL}/alunos/999')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json().get('erro'), 'Aluno não encontrado')

    def test_006_deleta_aluno_sucesso(self):
        # Cria um professor
        r_prof = requests.post(f'{self.BASE_URL}/professores', json={
            'nome': 'Prof. Ana',
            'idade': 40,
            'data_nascimento': '1984-03-20',
            'disciplina': 'Matemática',
            'salario': 5000
        })
        self.assertEqual(r_prof.status_code, 201)
        professor_id = r_prof.json().get('id')
        
        # Cria uma turma usando o professor criado
        r_turma = requests.post(f'{self.BASE_URL}/turmas', json={
            'nome': 'Turma A',
            'turno': 'Manhã',
            'professor_id': professor_id
        })
        self.assertEqual(r_turma.status_code, 201)
        turma_id = r_turma.json().get('id')
        
        # Cria o aluno usando os IDs válidos
        r_post = requests.post(f'{self.BASE_URL}/alunos', json={
            'nome': 'Marta',
            'data_nascimento': '1995-07-22',
            'nota_primeiro_semestre': 9.0,
            'nota_segundo_semestre': 8.5,
            'turma_id': turma_id,
            'professor_id': professor_id
        })
        self.assertEqual(r_post.status_code, 201)  # Verifica se o aluno foi criado com sucesso
        aluno_id = r_post.json().get('id')
        
        # Deleta o aluno criado
        r_delete = requests.delete(f'{self.BASE_URL}/alunos/{aluno_id}')
        self.assertEqual(r_delete.status_code, 200)
        self.assertEqual(r_delete.json().get('mensagem'), f'Aluno com ID {aluno_id} deletado')
        

    def test_007_deleta_aluno_inexistente(self):
        r = requests.delete(f'{self.BASE_URL}/alunos/999')  # ID inexistente
        self.assertIn(r.status_code, [400, 404])  # Verifica se o status é apropriado
        if r.headers.get('Content-Type') == 'application/json':
            self.assertEqual(r.json().get('erro'), 'Aluno não encontrado')
        else:
            self.fail("A resposta não contém um JSON válido")


    def test_008_edita_aluno_sucesso(self):
        # Cria um professor e uma turma antes de criar o aluno
        r_prof = requests.post(f'{self.BASE_URL}/professores', json={
        'nome': 'Prof. Ana',
        'idade': 40,
        'data_nascimento': '1984-03-20',
        'disciplina': 'Matemática',
        'salario': 5000
        })
        self.assertEqual(r_prof.status_code, 201)
        professor_id = r_prof.json().get('id')

        r_turma = requests.post(f'{self.BASE_URL}/turmas', json={
        'nome': 'Turma A',
        'turno': 'Manhã',
        'professor_id': professor_id
        })
        self.assertEqual(r_turma.status_code, 201)
        turma_id = r_turma.json().get('id')

        # Cria o aluno
        r_post = requests.post(f'{self.BASE_URL}/alunos', json={
        'nome': 'Lucas',
        'data_nascimento': '2000-01-01',
        'nota_primeiro_semestre': 8.0,
        'nota_segundo_semestre': 7.5,
        'turma_id': turma_id,
        'professor_id': professor_id
        })
        self.assertEqual(r_post.status_code, 201)
        aluno_id = r_post.json().get('id')

        # Edita o aluno criado
        r_put = requests.put(f'{self.BASE_URL}/alunos/{aluno_id}', json={'nome': 'Lucas Mendes'})
        self.assertEqual(r_put.status_code, 200)
        self.assertEqual(r_put.json().get('mensagem'), f'Aluno com ID {aluno_id} atualizado com sucesso')

        # Valida se a edição realmente ocorreu
        r_get = requests.get(f'{self.BASE_URL}/alunos/{aluno_id}')
        self.assertEqual(r_get.status_code, 200)
        self.assertEqual(r_get.json().get('nome'), 'Lucas Mendes')


    def test_009_edita_aluno_inexistente(self):
        r = requests.put(f'{self.BASE_URL}/alunos/999', json={'nome': 'Atualizado'})
        self.assertEqual(r.status_code, 404)  # Confirma que o status é 404
        if r.headers.get('Content-Type') == 'application/json':  # Checa se a resposta é JSON
            self.assertEqual(r.json().get('erro'), 'Aluno não encontrado')
        else:
            self.fail("A resposta não contém um JSON válido")  # Caso contrário, o teste falha


    def test_010_reseta_funciona(self):
        # Cria um aluno para garantir que há dados para resetar
        r_post = requests.post(f'{self.BASE_URL}/alunos', json={
            'nome': 'Cicero',
            'data_nascimento': '1997-02-02',
            'nota_primeiro_semestre': 6.5,
            'nota_segundo_semestre': 7.0,
            'turma_id': 1,  # Certifique-se de que o ID de turma existe
            'professor_id': 1  # Certifique-se de que o ID de professor existe
        })
        self.assertEqual(r_post.status_code, 201)  # Verifica se o aluno foi criado

        # Chama o endpoint de reset específico para alunos
        r_reset = requests.post(f'{self.BASE_URL}/reseta_alunos')
        self.assertEqual(r_reset.status_code, 200)  # Verifica que o reset foi bem-sucedido
        self.assertEqual(r_reset.json().get('mensagem'), 'Lista de alunos resetada com sucesso')  # Valida a mensagem

        # Verifica se a lista está vazia após o reset
        r_lista = requests.get(f'{self.BASE_URL}/alunos')
        self.assertEqual(r_lista.status_code, 200)  # A rota de listagem deve funcionar normalmente
        self.assertEqual(len(r_lista.json()), 0)  # Confirma que não há alunos após o reset


    # --- TESTES PARA /professores ---
    def test_100_professores_retorna_lista(self):
        r = requests.get(f'{self.BASE_URL}/professores')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(type(r.json()), list)

    def test_101_adiciona_professores(self):
        requests.post(f'{self.BASE_URL}/professores', json={
        'nome': 'Fernando',
        'idade': 40,
        'data_nascimento': '1982-05-15',
        'disciplina': 'Matemática',
        'salario': 3000
    })
        requests.post(f'{self.BASE_URL}/professores', json={
        'nome': 'Roberto',
        'idade': 45,
        'data_nascimento': '1977-04-10',
        'disciplina': 'História',
        'salario': 3500
    })
        r_lista = requests.get(f'{self.BASE_URL}/professores')
        lista_retornada = r_lista.json()
        self.assertTrue(any(professor['nome'] == 'Fernando' for professor in lista_retornada))
        self.assertTrue(any(professor['nome'] == 'Roberto' for professor in lista_retornada))

    def test_102_professores_por_id(self):
        # Cria um professor antes de buscá-lo
        r_post = requests.post(f'{self.BASE_URL}/professores', json={
            'nome': 'Mario',
            'idade': 50,
            'data_nascimento': '1973-03-12',
            'disciplina': 'Geografia',
            'salario': 4000
        })
        self.assertEqual(r_post.status_code, 201)  # Verifica se o professor foi criado com sucesso
    
        professor_id = r_post.json().get('id')  # Captura o ID do professor criado
    
        # Busca o professor criado pelo ID
        r_get = requests.get(f'{self.BASE_URL}/professores/{professor_id}')
        self.assertEqual(r_get.status_code, 200)  # Verifica que o status é 200
        self.assertEqual(r_get.json().get('nome'), 'Mario')  # Confirma que o nome é "Mario"


    def test_103_professores_reseta(self):
        # Cria um professor para garantir que há algo para resetar
        r_post = requests.post(f'{self.BASE_URL}/professores', json={
            'nome': 'Cicero',
            'idade': 35,
            'data_nascimento': '1988-02-02',
            'disciplina': 'Física',
            'salario': 3200
        })
        self.assertEqual(r_post.status_code, 201)  # Verifica se o professor foi criado com sucesso
    
        # Reseta os professores
        r_reset = requests.post(f'{self.BASE_URL}/reseta_professores')  # Chama a rota correta
        self.assertEqual(r_reset.status_code, 200)  # Verifica que o reset foi bem-sucedido
        self.assertEqual(r_reset.json().get('mensagem'), 'Lista de professores resetada com sucesso')  # Valida a mensagem
    
        # Verifica se a lista está vazia após o reset
        r_lista = requests.get(f'{self.BASE_URL}/professores')
        self.assertEqual(r_lista.status_code, 200)  # A rota de listagem ainda deve funcionar
        self.assertEqual(len(r_lista.json()), 0)  # Confirma que não há professores após o reset


    def test_104_deleta_professor(self):
        # Cria um professor antes de tentar deletá-lo
        r_post = requests.post(f'{self.BASE_URL}/professores', json={
            'nome': 'Lucas',
            'idade': 38,
            'data_nascimento': '1985-06-15',
            'disciplina': 'Química',
            'salario': 3000
        })
        self.assertEqual(r_post.status_code, 201)  # Verifica se o professor foi criado com sucesso
        professor_id = r_post.json().get('id')  # Captura o ID do professor criado
        
        # Tenta deletar o professor criado
        r_delete = requests.delete(f'{self.BASE_URL}/professores/{professor_id}')
        self.assertEqual(r_delete.status_code, 200)  # Verifica que a deleção foi bem-sucedida
        self.assertEqual(r_delete.json().get('mensagem'), f'Professor com ID {professor_id} deletado')
        
        # Confirma que o professor foi realmente deletado
        r_get = requests.get(f'{self.BASE_URL}/professores/{professor_id}')
        self.assertEqual(r_get.status_code, 404)  # O professor não deve mais existir
        

    def test_105_edita_professor(self):
        # Cria um professor antes de editá-lo
        r_post = requests.post(f'{self.BASE_URL}/professores', json={
            'nome': 'Lucas',
            'idade': 38,
            'data_nascimento': '1985-06-15',
            'disciplina': 'Química',
            'salario': 3000
        })
        self.assertEqual(r_post.status_code, 201)  # Verifica se o professor foi criado com sucesso
        professor_id = r_post.json().get('id')  # Captura o ID do professor criado
    
        # Edita o professor criado
        r_put = requests.put(f'{self.BASE_URL}/professores/{professor_id}', json={
            'nome': 'Lucas Mendes'
        })
        self.assertEqual(r_put.status_code, 200)  # Verifica se o status é 200
        self.assertEqual(r_put.json().get('mensagem'), f'Professor com ID {professor_id} atualizado com sucesso')
    
        # Valida a edição buscando o professor
        r_get = requests.get(f'{self.BASE_URL}/professores/{professor_id}')
        self.assertEqual(r_get.status_code, 200)  # Verifica que o status da busca é 200
        self.assertEqual(r_get.json().get('nome'), 'Lucas Mendes')  # Confirma que o nome foi atualizado



    def test_106_professor_id_inexistente(self):
        r = requests.get(f'{self.BASE_URL}/professores/999')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json().get('erro'), 'Professor não encontrado')

    


    def test_108_post_professor_sem_nome(self):
        r = requests.post(f'{self.BASE_URL}/professores', json={
            'idade': 30,
            'data_nascimento': '1993-01-01',
            'disciplina': 'Biologia',
            'salario': 2800
        })
        self.assertEqual(r.status_code, 400)  # Verifica que o status é 400 (Bad Request)
        self.assertEqual(r.json().get('erro'), "Campo obrigatório 'nome' está faltando")  # Mensagem atual da API



    # --- Testes Turma --- #
    def test_200_lista_turmas_vazia(self):
        r_lista = requests.get(f'{self.BASE_URL}/turmas')
        self.assertEqual(r_lista.status_code, 200)
        self.assertEqual(len(r_lista.json()), 0)

    def test_201_adiciona_turmas(self):
        requests.post(f'{self.BASE_URL}/turmas', json={
        'nome': 'Turma A',
        'turno': 'Manhã',
        'professor_id': 1
    })
        requests.post(f'{self.BASE_URL}/turmas', json={
        'nome': 'Turma B',
        'turno': 'Tarde',
        'professor_id': 2
    })
        r_lista = requests.get(f'{self.BASE_URL}/turmas')
        lista_retornada = r_lista.json()
        self.assertTrue(any(turma['nome'] == 'Turma A' for turma in lista_retornada))
        self.assertTrue(any(turma['nome'] == 'Turma B' for turma in lista_retornada))

    def test_202_turmas_por_id(self):
        r_post = requests.post(f'{self.BASE_URL}/turmas', json={
            'nome': 'Turma C',
            'turno': 'Noite',
            'professor_id': 1  # Certifique-se de que o professor com ID 1 existe
        })
        self.assertEqual(r_post.status_code, 201)  # Verifica se a turma foi criada com sucesso
    
        turma_id = r_post.json().get('id')  # Captura o ID da turma criada
    
        # Tenta buscar a turma recém-criada pelo ID
        r_get = requests.get(f'{self.BASE_URL}/turmas/{turma_id}')
        self.assertEqual(r_get.status_code, 200)  # Confirma que o status é 200 (Sucesso)
        self.assertEqual(r_get.json().get('nome'), 'Turma C')  # Valida o nome da turma


    def test_203_turmas_reseta(self):
        # Primeiro, cria uma turma para garantir que há algo para resetar
        r_post = requests.post(f'{self.BASE_URL}/turmas', json={
            'nome': 'Turma D',
            'turno': 'Manhã',
            'professor_id': 1  # Certifique-se de que o professor com ID 1 existe
        })
        self.assertEqual(r_post.status_code, 201)  # Verifica se a turma foi criada
    
        # Reseta as turmas
        r_reset = requests.post(f'{self.BASE_URL}/reseta_turmas')
        self.assertEqual(r_reset.status_code, 200)  # Verifica que o reset retorna sucesso
        self.assertEqual(r_reset.json().get('mensagem'), 'Lista de turmas resetada com sucesso')  # Valida a mensagem
    
        # Verifica se a lista está vazia após o reset
        r_lista = requests.get(f'{self.BASE_URL}/turmas')
        self.assertEqual(r_lista.status_code, 200)  # A rota de listagem ainda deve funcionar
        self.assertEqual(len(r_lista.json()), 0)  # Confirma que não há turmas após o reset

    def test_204_deleta_turma(self):
        # Primeiro, cria uma turma
        r_post = requests.post(f'{self.BASE_URL}/turmas', json={
            'nome': 'Turma E',
            'turno': 'Tarde',
            'professor_id': 1  # Certifique-se de que o professor com ID 1 existe
        })
        self.assertEqual(r_post.status_code, 201)  # Verifica se a turma foi criada
    
        turma_id = r_post.json().get('id')  # Captura o ID da turma criada
    
        # Em seguida, tenta deletar a turma
        r_delete = requests.delete(f'{self.BASE_URL}/turmas/{turma_id}')
        self.assertEqual(r_delete.status_code, 200)  # Verifica se o status da exclusão é 200
        self.assertEqual(r_delete.json().get('mensagem'), f'Turma com ID {turma_id} deletada')
    
        # Por fim, valida se a turma realmente foi deletada
        r_get = requests.get(f'{self.BASE_URL}/turmas/{turma_id}')
        self.assertEqual(r_get.status_code, 404)  # A turma não deve mais existir


    def test_205_edita_turma(self):
    # Primeiro, cria uma turma
        r_post = requests.post(f'{self.BASE_URL}/turmas', json={
            'nome': 'Turma F',
            'turno': 'Noite',
            'professor_id': 1  # Certifique-se de que o professor com ID 1 existe
        })
        self.assertEqual(r_post.status_code, 201)  # Verifica se a turma foi criada com sucesso
    
        turma_id = r_post.json().get('id')  # Captura o ID da turma criada
    
        # Em seguida, tenta editar a turma criada
        r_put = requests.put(f'{self.BASE_URL}/turmas/{turma_id}', json={
            'nome': 'Turma F Atualizada'
        })
        self.assertEqual(r_put.status_code, 200)  # Verifica se o status da atualização é 200
        self.assertEqual(r_put.json().get('mensagem'), f'Turma com ID {turma_id} atualizada com sucesso')
    
        # Por fim, valida se a edição realmente ocorreu
        r_get = requests.get(f'{self.BASE_URL}/turmas/{turma_id}')
        self.assertEqual(r_get.status_code, 200)  # A turma ainda deve existir
        self.assertEqual(r_get.json().get('nome'), 'Turma F Atualizada')


    def test_206_turma_id_inexistente(self):
        r = requests.get(f'{self.BASE_URL}/turmas/999')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json().get('erro'), 'Turma não encontrada')





    def test_208_turmas_nao_confundir_com_professores(self):
        # Reset do ambiente para limpar professores e turmas
        r_reset_professores = requests.post(f'{self.BASE_URL}/reseta_professores')
        self.assertEqual(r_reset_professores.status_code, 200)
    
        r_reset_turmas = requests.post(f'{self.BASE_URL}/reseta_turmas')
        self.assertEqual(r_reset_turmas.status_code, 200)
    
        # Adiciona um professor
        r_professor = requests.post(f'{self.BASE_URL}/professores', json={
            'nome': 'Fernando',
            'idade': 40,
            'data_nascimento': '1982-05-15',
            'disciplina': 'Matemática',
            'salario': 3000
        })
        self.assertEqual(r_professor.status_code, 201)  # Verifica se o professor foi criado com sucesso
    
        # Adiciona uma turma
        r_turma = requests.post(f'{self.BASE_URL}/turmas', json={
            'nome': 'Turma H',
            'turno': 'Tarde',
            'professor_id': r_professor.json().get('id')  # Usa o ID do professor criado
        })
        self.assertEqual(r_turma.status_code, 201)  # Verifica se a turma foi criada com sucesso
    
        # Verifica se há exatamente 1 professor e 1 turma
        r_lista_professores = requests.get(f'{self.BASE_URL}/professores')
        self.assertEqual(r_lista_professores.status_code, 200)
        self.assertEqual(len(r_lista_professores.json()), 1)  # Deve haver apenas 1 professor
    
        r_lista_turmas = requests.get(f'{self.BASE_URL}/turmas')
        self.assertEqual(r_lista_turmas.status_code, 200)
        self.assertEqual(len(r_lista_turmas.json()), 1)  # Deve haver apenas 1 turma



if __name__ == '__main__':
    unittest.main()