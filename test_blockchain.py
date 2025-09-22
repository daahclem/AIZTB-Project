from blockchain.blockchain_api import log_access_decision, get_log, get_log_count

# Log a new access decision
receipt = log_access_decision("user42", "start_charging", "approved", "0.12")
print("✅ Access logged:", receipt.transactionHash.hex())

# Get total logs
count = get_log_count()
print("📊 Total Logs:", count)

# Retrieve a log entry
log = get_log(0)
print("📄 Log[0]:", log)
