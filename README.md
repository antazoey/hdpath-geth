# hdpath-geth

Starts an ephemeral geth with accounts generated from a HD Path.
None of the blockchain data persists on restart. This project is useful for testing.

## Install

Use a virtual environment and install from necessary requirements:

```bash
pip install -r requirements.txt
```

## Start

```bash
make
```

Optionally, set a `MNEMONIC` arg as well as `NUM_OF_ACCOUNTS` when calling `make`.
