import json
from web3 import Web3
from pathlib import Path

# Load ABI and bytecode
abi = json.loads(Path("blockchain/AccessControlLogs.abi.json").read_text())
bytecode = Path("blockchain/AccessControlLogs.bytecode").read_text()

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Use unlocked Ganache account
w3.eth.default_account = w3.eth.accounts[0]

# Deploy
AccessControlLogs = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = AccessControlLogs.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Save deployed address
Path("blockchain/deployed_address.txt").write_text(tx_receipt.contractAddress)

print(f"✅ Deployed at: {tx_receipt.contractAddress}")
