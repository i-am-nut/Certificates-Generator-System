from flask import Flask
from flask import send_file, render_template
from flask_restful import reqparse, abort, Api, Resource
import transactions
from pathlib import Path

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('user_private_key')
parser.add_argument('private_key')
parser.add_argument('full_name')
parser.add_argument('cpf')
parser.add_argument('course_name')

class Database(Resource):
    def get(self):
        return render_template('index.html')
        #visualizacao da pagina do sistema gerador de certificado
        #retornar aqui a pagina principal com as forms para insercao dos dados do usuario
        
    def post(self):
        args = parser.parse_args()
        if args['user_private_key'] == 'marco_aurelio_key' or args['user_private_key'] == 'graca_key':
            pk = transactions.create_user(args['full_name'], args['cpf'], args['course_name'])
            return pk
        else:
            return 'you are not allowed to create a user'
        #criacao de usuario
        #SOMENTE 2 PESSOAS (DIRETOR, DESENVOLVIMENTO) PODEM CRIAR USUARIO
        #receber nome todo, cpf e nome do curso
        #chamar funcao de criacao de usuario (do banco) passando os parametros recebidos
        #retorna o cliente sua chave privada

    def put(self):
        args = parser.parse_args()
        result = transactions.generate_cert(args['full_name'], args['cpf'], args['course_name'], args['private_key'])
        return send_file(str(Path.cwd())+'/certificates/'+result+'.pdf',attachment_filename = '{}.pdf'.format(args['cpf']))
        #receber nome todo, cpf, nome do curso e a chave privada do usuario
        #retorna o certificado aberto em outra pagina?
        #fazer o cliente baixar o arquivo de certificado gerado?
        #test user= {pvk: GwYM3fNf7Lq2RfvKhQWkRfEpENFxu5cK93L8uPDAc3WU, name=nego drama, course_name=photoshop, cpf=123123}
        

##
## Actually setup the Api resource routing here
##
api.add_resource(Database, '/apiv1')


if __name__ == '__main__':
    app.run(debug=True)

