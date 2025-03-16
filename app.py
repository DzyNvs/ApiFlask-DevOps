from flask import Flask, jsonify, make_response, request 
from bd import Alunos

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/Alunos', methods=['POST'])
def create_Alunos():
    alunos = request.json
    Alunos.append(alunos)   
    return make_response (
        jsonify(Alunos)
    )
    
    

@app.route('/Alunos', methods=['GET'])
def get_Alunos():
    return make_response (
        jsonify(Alunos)
    )


@app.route('/Alunos', methods=['DELETE'])
def delete_Alunos():
    

if __name__  == '__main__': 
    app.run(debug=True)