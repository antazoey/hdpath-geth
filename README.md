# hdpath-geth

Starts an ephemeral geth with accounts generated from a HD Path.
None of the blockchain data persists on restart. This project is useful for testing.

## Dependencies

Currently, only claiming to support python 3.9.7 and geth version 1.10.10 
but will probably work on other versions as well.

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
