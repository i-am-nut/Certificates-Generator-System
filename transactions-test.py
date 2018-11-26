from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from time import sleep
from sys import exit
import datetime


user_name_keypair, bob, carol= generate_keypair(), generate_keypair(), generate_keypair() 

bdb_root_url = 'https://test.bigchaindb.com' 
bdb = BigchainDB(bdb_root_url)

#recebendo um usuario para ser inserido no banco

def create_user(user_fullname, cpf):
    user_fullname = #recebe da form
    cpf = #recebe da form
    user_name_keypair = generate_keypair()
    
    #retornar para o usuario sua chave privada
    
    subscriber_asset = {
        'data': {
            'aluno': {
                'nome': user_fullname,
                'cpf': cpf,
                'public_key': user_name_keypair.public_key()
            },
        },
    }
    
    subscriber_asset_metadata = {
        'timestamp': str(datetime.datetime.now()).split('.')[0] 
    }
    
    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=user_name_keypair.public_key,
        asset=subscriber_asset,
        metadata=subscriber_asset_metadata
    )
    
    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=user_name_keypair.private_key
    )
    
    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

############################################################################

#emissão de um certificado
#recebe o nome completo de usuario e a PK
#??? fazer pesquisa por asset ou transaction???

def generate_cert(user_fullname,user_name_private_key):
    user_data = bdb.assets.get(search=user_fullname)
    
    user_name = user_data[0]['data']['aluno']['nome']
    id_creation_to_generate_certificate = user_data[0]['id']
    
    user_blockchain = bdb.transactions.get(asset_id=id_creation_to_generate_certificate)
    
    len(user_blockchain)
    
    private_key = #recebida do post
    
    #txid = fulfilled_creation_tx['id'] 
    #bdb.assets.get(search='meu nome')
    
    asset_id = txid
    
    transfer_asset = {
        'id': asset_id #sempre o id da operação de criação
    }
    
    
    subscriber_asset_metadata = {
        'timestamp': str(datetime.datetime.now()).split('.')[0] 
    }
    
    
    output_index = 0
    output = user_blockchain[len(user_blockchain)-1]['outputs'][output_index]
    #output = fulfilled_creation_tx['outputs'][output_index]
    
    transfer_input = {
        'fulfillment': output['condition']['details'],
        'fulfills': {
            'output_index': output_index,
            'transaction_id': user_blockchain[len(user_blockchain)-1]['id'] 
            #'transaction_id': fulfilled_creation_tx['id']
        },
        'owners_before': output['public_keys']
    }
    
    prepared_transfer_tx = bdb.transactions.prepare(
        operation='TRANSFER',
        asset=transfer_asset,
        inputs=transfer_input,
        metadata=subscriber_asset_metadata
        recipients=user_name_keypair.public_key,
    )
    
    fulfilled_transfer_tx = bdb.transactions.fulfill(
        prepared_transfer_tx,
        private_keys=user_name_keypair.private_key,
    )
    
    sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)
    
    #encaixar aqui função de gerar o certificado

'''
print("Is Bob the owner?",
    sent_transfer_tx['outputs'][0]['public_keys'][0] == bob.public_key)

print("Was Alice the previous owner?",
    fulfilled_transfer_tx['inputs'][0]['owners_before'][0] == user_name_keypair.public_key)
'''

##########################################################################



update_asset_metadata = {
    'planet': 'pluto',
    'timestamp': str(datetime.datetime.now()).split('.')[0] 
}



output2 = fulfilled_transfer_tx['outputs'][output_index]

transfer_input2 = {
    'fulfillment': output2['condition']['details'],
    'fulfills': {
        'output_index': output_index,
        'transaction_id': fulfilled_transfer_tx['id']
    },
    'owners_before': output2['public_keys']
}

prepared_transfer_tx2 = bdb.transactions.prepare(
    operation='TRANSFER',
    asset=transfer_asset,
    inputs=transfer_input2,
    recipients=carol.public_key,
    metadata=update_asset_metadata
)

fulfilled_transfer_tx2 = bdb.transactions.fulfill(
    prepared_transfer_tx2,
    private_keys=bob.private_key,
)

sent_transfer_tx2 = bdb.transactions.send_commit(fulfilled_transfer_tx2)


print("Is Carol the owner?",
    sent_transfer_tx2['outputs'][0]['public_keys'][0] == carol.public_key)

print("Was Bob the previous owner?",
    fulfilled_transfer_tx2['inputs'][0]['owners_before'][0] == bob.public_key)



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
