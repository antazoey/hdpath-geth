#!/bin/bash

set -e

clean() {
  blockchain_path="${1:-blockchain}"
  rm -rf "${blockchain_path}/"
}

create_genesis_json() {
  num_accounts="${1:?num accounts required at arg 1.}"
  mnemonic="${2:?Mnemonic required at arg 2.}"
  python scripts/create_genesis_file.py "${num_accounts}" "${mnemonic}"
}

init_blockchain() {
  num_accounts="${1:?num accounts required at arg 1.}"
  mnemonic="${2:?Mnemonic required at arg 2.}"
  rm -rf pwd_file
  echo "this-is-not-a-secure-password" >> pwd_file
  create_genesis_json "${num_accounts}" "${mnemonic}"
  geth --datadir "${blockchain_path}" init ./genesis.json

  # A least one account must exist for mining to work
  geth --datadir "${blockchain_path}" --password pwd_file account new
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
  num_accounts="${2:-10}"
  mnemonic="${3:-test test test test test test test test test test test junk}"
  clean "${blockchain_path}"
  init_blockchain "${num_accounts}" "${mnemonic}"
  start "${blockchain_path}"
}

main "$@"
