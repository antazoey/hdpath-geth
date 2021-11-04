#!/bin/bash

set -e

clean() {
  blockchain_path="${1:-blockchain}"
  rm -rf "${blockchain_path}/"
}

init_blockchain() {
  blockchain_path="${1:-blockchain}"
  mnemonic="${2:?Mnemonic required at arg 1.}"
  num_accounts="${3:?num accounts required at arg 2.}"
  consensus="${4:?The consensus algorithm requires at arg 3.}"
  create_pwd_file
  create_miner_account "${blockchain_path}" 
  create_genesis_json "${blockchain_path}" "${mnemonic}" "${num_accounts}" "${consensus}"
  geth --datadir "${blockchain_path}" init ./genesis.json
}

create_pwd_file() {
  rm -rf pwd_file
  echo "this-is-not-a-secure-password" >> pwd_file
}

create_miner_account() {
  blockchain_path="${1:-blockchain}"
  geth --datadir "${blockchain_path}" --password pwd_file account new
}

create_genesis_json() {
  blockchain_path="${1:-blockchain}"
  mnemonic="${2:?Mnemonic required at arg 2.}"
  num_accounts="${3:?num accounts required at arg 3.}"
  consensus="${4:?The consensus algorithm requires at arg 4.}"
  python scripts/create_genesis_file.py "${blockchain_path}" "${mnemonic}" "${num_accounts}" "${consensus}"
}

start() {
  blockchain_path="${1:-blockchain}"
  geth \
    --http \
    --http.addr localhost \
    --http.port 8545 \
    --http.api admin,debug,eth,miner,net,personal,txpool,web3 \
    --ws \
    --ws.addr 127.0.0.1 \
    --ws.port 8546 \
    --ws.api admin,debug,eth,miner,net,personal,txpool,web3 \
    --datadir $blockchain_path \
    --maxpeers 0 \
    --networkid 1337 \
    --port 30303 \
    --ipcpath $blockchain_path/geth.ipc \
    --verbosity 5 \
    --unlock 0 \
    --password pwd_file \
    --nodiscover \
    --mine \
    --miner.threads 1 \
    --allow-insecure-unlock
}

main() {
  blockchain_path="${1:-blockchain}"
  mnemonic="${2:-test test test test test test test test test test test junk}"
  num_accounts="${3:-10}"
  consensus="${4:pow}"
  clean "${blockchain_path}"
  init_blockchain "${blockchain_path}" "${mnemonic}" "${num_accounts}" "${consensus}"
  start "${blockchain_path}"
}

main "$@"
