MNEMONIC = "test test test test test test test test test test test junk"
NUM_OF_ACCOUNTS = 10
BLOCKCHAIN_DIR = blockchain
CONSENSUS = pow

ephemeral_geth::
	@scripts/start.sh $(BLOCKCHAIN_DIR) $(MNEMONIC) $(NUM_OF_ACCOUNTS) $(CONSENSUS)


attach::
	@geth attach $(BLOCKCHAIN_DIR)/geth.ipc
