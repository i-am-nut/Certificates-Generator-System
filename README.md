# Certificates-Generator-System
A system created for the generation of certificates from worshops and lectures held at CTIC - Coordenadoria de Internet e Data Center

Check the `Wiki` page for the draft of the aims, enhancements and operation of this system. 


# Database Usage

There's two functions created for the database: `create_user` and `generate_cert`

To create a user, one need to pass as argument to function his `Full Name, CPF and the name of the course` he is attending to.
After the execution, the Private Key of the user is returned, which should be saved somewhere to generate his cert futurelly.

As for `generate_cert`, one has to pass user `Full Name, CPF, course's name and his private key` to validate the transaction at the database and afterwards generate his certificate. The certificate is identified by user's CPF and stored on a directory called `certificates/` on the current script directory;the function returns a OK message at the end.

# Deploy BigchainDB Network

- Docker:
```
$ docker pull bigchaindb/bigchaindb:all-in-one

$ docker run \
  --detach \
  --name bigchaindb \
  --publish 9984:9984 \
  --publish 9985:9985 \
  --publish 27017:27017 \
  --publish 26657:26657 \
  --volume $HOME/bigchaindb_docker/mongodb/data/db:/data/db \
  --volume $HOME/bigchaindb_docker/mongodb/data/configdb:/data/configdb \
  --volume $HOME/bigchaindb_docker/tendermint:/tendermint \
  bigchaindb/bigchaindb:all-in-one

```
There's also a `docker-compose.yaml` in BigchainDB repo that easily deploys a one-node BigchainDB network.

For a 4 nodes network, check `stack.sh` script on BigchainDB repo.

https://docs.bigchaindb.com/projects/contributing/en/latest/dev-setup-coding-and-contribution-process/run-dev-network-stack.html#download-the-scripts

- Kubernetes / Helm

 `helm install --name bdb k8/bdb/`
