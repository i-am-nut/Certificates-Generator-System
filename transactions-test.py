from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from time import sleep
from sys import exit
import datetime


alice, bob, carol= generate_keypair(), generate_keypair(), generate_keypair() 

bdb_root_url = 'https://test.bigchaindb.com' 
bdb = BigchainDB(bdb_root_url)

#recebendo um usuario para ser inserido no banco

bicycle_asset = {
    'data': {
        'aluno': {
            'nome': 'emerson',
            'cpf': '123123123'
        },
    },
}

bicycle_asset_metadata = {
    'planet': 'earth'
}

prepared_creation_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset=bicycle_asset,
    metadata=bicycle_asset_metadata
)

fulfilled_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx,
    private_keys=alice.private_key
)

sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

############################################################################

#emissão de um certificado
#recebe o nome completo de usuario e a PK
#??? fazer pesquisa por asset ou transaction???

user_data = bdb.assets.get(search='NOME-DO-USUARIO')

user_data[0]['data']['aluno']['nome']
private_key = #recebida do post

txid = fulfilled_creation_tx['id']

asset_id = txid

transfer_asset = {
    'id': asset_id
}

output_index = 0
output = fulfilled_creation_tx['outputs'][output_index]

transfer_input = {
    'fulfillment': output['condition']['details'],
    'fulfills': {
        'output_index': output_index,
        'transaction_id': fulfilled_creation_tx['id']
    },
    'owners_before': output['public_keys']
}

prepared_transfer_tx = bdb.transactions.prepare(
    operation='TRANSFER',
    asset=transfer_asset,
    inputs=transfer_input,
    recipients=bob.public_key,
)

fulfilled_transfer_tx = bdb.transactions.fulfill(
    prepared_transfer_tx,
    private_keys=alice.private_key,
)

sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)

print("Is Bob the owner?",
    sent_transfer_tx['outputs'][0]['public_keys'][0] == bob.public_key)

print("Was Alice the previous owner?",
    fulfilled_transfer_tx['inputs'][0]['owners_before'][0] == alice.public_key)


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
