import collections
import json
from pathlib import Path
import sys
from typing import Tuple

from eth_account import Account
from eth_account.hdaccount import HDPath, seed_from_mnemonic
from eth_utils import to_wei
from hexbytes import HexBytes

_BASE_GENESIS_DATA = {
    "coinbase": "0x0000000000000000000000000000000000000000",
    "nonce": "0xdeadbeefdeadbeef",
    "timestamp": "0x0",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "gasLimit": "0x0",
    "difficulty": "0x0",
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "config": {
        "chainId": 1337,
        "gasLimit": 0,
        "homesteadBlock": 0,
        "difficulty": "0x0",
        "eip150Block": 0,
        "eip155Block": 0,
        "eip158Block": 0,
        "byzantiumBlock": 0,
        "constantinopleBlock": 0,
        "petersburgBlock": 0,
        "istanbulBlock": 0,
        "berlinBlock": 0,
        "londonBlock": 0,
    },
}


class UsageError(Exception):
    def __init__(self, message: str = None):
        message = message or "BAD USAGE"
        usage = (
            f"{message} Usage:\n\t"
            "python scripts/create_genesis_file.py [integer] "
            "'test test test test test test test test test test test junk' "
            "[poa|pow]"
        )
        super().__init__(usage)


def _parse_args(argv) -> Tuple[int, str]:
    if len(sys.argv) < 5:
        raise UsageError("Wrong number of arguments.")
    
    data_dir = sys.argv[1]

    mnemonic = sys.argv[2]

    number_of_accounts = sys.argv[3]
    if not number_of_accounts.isnumeric():
        raise UsageError(f"Number of accounts ('{number_of_accounts}') is not numeric.")

    number_of_accounts = int(number_of_accounts)

    consensus = sys.argv[4].lower()
    if consensus not in ["poa", "pow"]:
        raise UsageError(
            f"Consensus algorithm '{consensus}' is not supported. Must be one of [poa|pow]."
        )

    return data_dir, mnemonic, number_of_accounts, consensus


GeneratedDevAccount = collections.namedtuple(
    "GeneratedDevAccount", ("address", "private_key")
)


def _create_accounts(
    mnemonic: str, number_of_accounts: int, hd_path_format="m/44'/60'/0'/{}"
):
    seed = seed_from_mnemonic(mnemonic, "")
    accounts = []

    for i in range(0, number_of_accounts):
        hd_path = HDPath(hd_path_format.format(i))
        private_key = HexBytes(hd_path.derive(seed)).hex()
        address = Account.from_key(private_key).address
        accounts.append(GeneratedDevAccount(address, private_key))

    return accounts


def _create_genesis_json(data_dir: str, accounts: GeneratedDevAccount, consensus: str = "pow"):
    genesis_data = dict(_BASE_GENESIS_DATA)
    if consensus.lower() == "pow":
        genesis_data["config"]["ethash"] = {}
    elif consensus.lower() == "poa":
        genesis_data["config"]["clique"] = {"period": 0, "epoch": 3000}
        sealer = _get_miner_address(data_dir)
        genesis_data["extraData"] = f"0x{'0' * 64}{sealer}{'0' * 130}"

    genesis_data["alloc"] = {
        a.address: {"balance": str(to_wei(10000, "ether"))} for a in accounts
    }

    return genesis_data


def _get_miner_address(data_dir: str) -> str:
    key_store_path = Path(data_dir) / "keystore"
    key_file_path = next(key_store_path.iterdir())
    with open(key_file_path) as key_file:
        key_data = json.load(key_file)
        return key_data["address"].replace("0x", "")


def create_genesis_json(data_dir: str, mnemonic: str, number_of_accounts: int, consensus: str):
    genesis_path = Path("genesis.json")
    if genesis_path.exists():
        genesis_path.unlink()

    accounts = _create_accounts(mnemonic, number_of_accounts)
    genesis_json = _create_genesis_json(data_dir, accounts, consensus=consensus)

    with open(genesis_path, "w") as genesis_file:
        json.dump(genesis_json, genesis_file, indent=2)


if __name__ == "__main__":
    data_dir, mnemonic, number_of_accounts, consensus = _parse_args(sys.argv)
    create_genesis_json(data_dir, mnemonic, number_of_accounts, consensus)
