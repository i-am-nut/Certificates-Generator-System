from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

#bdb_root_url = 'http://200.239.64.46:30080'
bdb_root_url = 'http://10.15.10.2:9984'
#bdb_root_url = 'http://localhost:9984'
bdb = BigchainDB(bdb_root_url)

msg = 'bigchaindb esta funcionando'

alice = generate_keypair()
tx = bdb.transactions.prepare(
            operation='CREATE',
                signers=alice.public_key,
                    asset={'data': {'message': msg}})
signed_tx = bdb.transactions.fulfill(
            tx,
                private_keys=alice.private_key)
bdb.transactions.send_commit(signed_tx) # write
block_height = bdb.blocks.get(txid=signed_tx['id'])
block = bdb.blocks.retrieve(str(block_height)) # read
print(block)

