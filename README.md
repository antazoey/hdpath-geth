# hdpath-geth

Starts an ephemeral geth with accounts generated from a HD Path.
Every time it is started, it deletes the old data first.

## Install

pip install -r requirements.txt

## Start

```bash
make
```

Optionally, set a `MNEMONIC` arg as well as `NUM_OF_ACCOUNTS` when calling `make`.
