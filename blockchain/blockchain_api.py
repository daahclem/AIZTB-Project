
from web3 import Web3
import json

# Load deployed address
with open("blockchain/deployed_address.txt", "r") as f:
    contract_address = f.read().strip()

# Load ABI
with open("blockchain/AccessControlLogs.abi.json", "r") as f:
    abi = json.load(f)

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
web3.eth.default_account = web3.eth.accounts[0]

contract = web3.eth.contract(address=contract_address, abi=abi)

# Function to log a decision to blockchain
def log_access_decision(user_id, action, decision, risk_score):
    tx = contract.functions.addLog(
        user_id,
        action,
        decision,
        str(risk_score)
    ).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx)
    return receipt

def get_log(index):
    return contract.functions.getLog(index).call()
