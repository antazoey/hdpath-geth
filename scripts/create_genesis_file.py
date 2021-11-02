import collections
import json
from pathlib import Path
import sys
from typing import Tuple

from eth_account import Account
from eth_account.hdaccount import HDPath, seed_from_mnemonic
from eth_utils import to_wei
from hexbytes import HexBytes


class UsageError(Exception):
    def __init__(self):
        usage = (
            "python scripts/create_genesis_file.py 10 "
            "'test test test test test test test test test test test junk'"
        )
        super().__init__(usage)


def _parse_args(argv) -> Tuple[int, str]:
    if len(sys.argv) < 3:
        raise UsageError()

    number_of_accounts = sys.argv[1]
    if not number_of_accounts.isnumeric():
        raise UsageError()
    
    number_of_accounts = int(number_of_accounts)
    mnemonic = sys.argv[2]
    return number_of_accounts, mnemonic


GeneratedDevAccount = collections.namedtuple(
    "GeneratedDevAccount", ("address", "private_key")
)


def create_genesis_json(
    number_of_accounts: int,
    mnemonic: str,
    hd_path_format="m/44'/60'/0'/{}",
):
    """
    Creates account for using in chain genesis.
    """
    seed = seed_from_mnemonic(mnemonic, "")
    accounts = []

    for i in range(0, number_of_accounts):
        hd_path = HDPath(hd_path_format.format(i))
        private_key = HexBytes(hd_path.derive(seed)).hex()
        address = Account.from_key(private_key).address
        accounts.append(GeneratedDevAccount(address, private_key))

    alloc_entries = {
        a.address: {"balance": str(to_wei(10000, "ether"))} for a in accounts
    }

    genesis_path = Path("genesis.json")
    if genesis_path.exists():
        genesis_path.unlink()

    genesis_json = {
        "coinbase": "0x0000000000000000000000000000000000000000",
        "nonce": "0xdeadbeefdeadbeef",
        "timestamp": "0x0",
        "parentHash":"0x0000000000000000000000000000000000000000000000000000000000000000",
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
            "ethash": {},
        },
        "alloc": alloc_entries,
    }
    with open(genesis_path, "w") as genesis_file:
        json.dump(genesis_json, genesis_file, indent=2)


if __name__ == "__main__":
    number_of_accounts, mnemonic = _parse_args(sys.argv)
    create_genesis_json(number_of_accounts, mnemonic)
