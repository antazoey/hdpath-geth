MNEMONIC = "test test test test test test test test test test test junk"
NUM_OF_ACCOUNTS = 10
BLOCKCHAIN_DIR = blockchain

ephemeral_geth::
	@scripts/start.sh $(BLOCKCHAIN_DIR) $(NUM_OF_ACCOUNTS) $(MNEMONIC)


attach::
	@geth attach $(BLOCKCHAIN_DIR)/geth.ipc
