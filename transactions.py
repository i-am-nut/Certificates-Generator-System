from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from time import sleep
from sys import exit
import datetime
import certificator


bdb_root_url = 'https://test.bigchaindb.com' 
bdb = BigchainDB(bdb_root_url)


#criando um usuario no banco
#eh preciso do seu nome completo, cpf e nome do curso a ser assistido
#ao final retorna para o usuario sua chave privada
def create_user(user_fullname, cpf, course_name):
    
    print('generating keypair')
    user_name_keypair = generate_keypair()
    
    print('assembling subscriber_asset')
    subscriber_asset = {
        'data': {
            'aluno': {
                'nome': user_fullname,
                'cpf': cpf,
                'course_name': course_name,
                'public_key': user_name_keypair.public_key
            },
        },
    }
    
    print('assembling subscriber_asset')
    subscriber_asset_metadata = {
        'timestamp': 'usuario criado em '+str(datetime.datetime.now()).split('.')[0] 
    }
    
    print('preparing create transaction')
    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=user_name_keypair.public_key,
        asset=subscriber_asset,
        metadata=subscriber_asset_metadata
    )
    
    print('fulfilling create transaction')
    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=user_name_keypair.private_key
    )
    
    print('commiting create transaction')
    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

    print('succesfully user created')
    print('write your private key below somewhere and hide it behind seven keys!')

    #retornar para o usuario sua chave privada
    return user_name_keypair.private_key

#emissão de um certificado
#recebe o nome completo de usuario, cpf a private key
#para gerar um certificado eh preciso do nome do usuario, cpf, curso e chave privada
#pois o mesmo usuario pode ter se inscrito em diferentes cursos
#neste caso, a diferença será o nome do curso

def generate_cert(user_fullname, cpf, course_name, user_name_private_key):

    #melhorar esse limite, o banco pode ficar gigante!!!
    print('searching for asset with the User credentials')
    user_data = bdb.assets.get(search=user_fullname, limit=10)
    
    print('looping through the data gathered and saving the exactly wanted one')
    try:
        for index_list in range(0,len(user_data)):
            user_name = user_data[index_list]['data']['aluno']['nome']
            user_cpf = user_data[index_list]['data']['aluno']['cpf']
            user_course_name = user_data[index_list]['data']['aluno']['course_name']
            user_public_key = user_data[index_list]['data']['aluno']['public_key']
            id_creation_to_generate_certificate = user_data[index_list]['id']

            if user_name == user_fullname and user_cpf == cpf and user_course_name == course_name:
                break

    except KeyError:
        pass

    if user_fullname != user_name or cpf != user_cpf or course_name != user_course_name:
        return 'the credentials were not found'

    print('getting the user blockchain')
    user_blockchain = bdb.transactions.get(asset_id=id_creation_to_generate_certificate)
    
    asset_id = id_creation_to_generate_certificate
    
    print('setting transfer asset')
    transfer_asset = {
        'id': asset_id #sempre o id da operação de criação
    }
    
    
    print('setting metadata for this transaction')
    subscriber_asset_metadata = {
        'timestamp': 'certificado gerado em '+str(datetime.datetime.now()).split('.')[0] 
    }
    
    
    output_index = 0
    output = user_blockchain[len(user_blockchain)-1]['outputs'][output_index]
    
    print('setting transfer input')
    transfer_input = {
        'fulfillment': output['condition']['details'],
        'fulfills': {
            'output_index': output_index,
            'transaction_id': user_blockchain[len(user_blockchain)-1]['id'] 
        },
        'owners_before': output['public_keys']
    }
    
    print('preparing transfer transaction')
    prepared_transfer_tx = bdb.transactions.prepare(
        operation='TRANSFER',
        asset=transfer_asset,
        inputs=transfer_input,
        metadata=subscriber_asset_metadata,
        recipients=user_public_key,
    )
    
    try:
        print('fulfilling transfer transaction')
        fulfilled_transfer_tx = bdb.transactions.fulfill(
            prepared_transfer_tx,
            private_keys=user_name_private_key,
        )
    
    except Exception as e:
        return e
    
    print('commiting transfer transaction')
    sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)

    print('generating user certificate')
    certificator.make_certi(cpf, user_fullname, project=user_course_name)
    
    return 'certificate generated succesfully'


if __name__ == '__main__':
    pass

'''
trials = 0

while trials < 100:
    try:
        if bdb.transactions.status(txid).get('status') == 'valid':
        break
    except bigchaindb_driver.exceptions.NotFoundError:
        trials += 1
        print(bdb.transactions.status(txid))
'''
