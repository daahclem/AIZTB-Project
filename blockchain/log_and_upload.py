import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ipfs_utils import upload_to_ipfs, get_ipfs_url

from blockchain.ipfs_utils import upload_to_ipfs, get_ipfs_url
from blockchain.blockchain_api import log_access_decision
from blockchain.ipfs_utils import upload_to_ipfs, get_ipfs_url
from blockchain.blockchain_api import log_access_decision

log_file_path = "logs/sim_with_ai.csv"

# 1. Upload to IPFS
cid = upload_to_ipfs(log_file_path)
if not cid:
    print("❌ Failed to upload to IPFS.")
    exit()

print(f"✅ Uploaded to IPFS. CID: {cid}")
print(f"🌐 IPFS URL: {get_ipfs_url(cid)}")

# 2. Log CID on Ethereum
receipt = log_access_decision(
    user_id="evuser001",
    action="log_upload",
    decision=cid,
    risk_score="0.3"
)

print(f"✅ Transaction hash: {receipt.transactionHash.hex()}")
