from flask import Flask, jsonify, request

dici= {
    "alunos":[
        {"id":1,"nome":"caio"}
    ],
    "professores":[],
    "turma":[]
}

app = Flask(__name__)

class AlunoNaoExiste(Except):
    pass

@app.route('/',methods=['GET'])
def getIndex():
    dados={"msg":"Hello World!!!"}
    return jsonify(dados), 200

@app.route("/alunos", methods=['GET'])
def gteAluno():
    dados = dici["alunos"]
    return jsonify(dados)

@app.route("/alunos", methods=['POST'])
def createAluno():
    dados = request.json
    dici["alunos"].append(dados)
    return jsonify(dados)

@app.route("/alunos/<int:idAluno>", methods=['PUT'])
def updateAluno(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dados = request.json
            aluno['nome']= dados['nome']
            return jsonify(dados)
        else:
            return jsonify("aluno não encontrado"),404
   
if __name__ == '__main__':
    app.run(debug=True)