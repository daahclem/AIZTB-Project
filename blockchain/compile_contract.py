import json
from solcx import install_solc, compile_standard
from pathlib import Path

# Install Solidity compiler
install_solc("0.8.0")

# Read contract
contract_path = Path("blockchain/contracts/AccessControlLogs.sol")
source_code = contract_path.read_text()

# Compile
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "AccessControlLogs.sol": {"content": source_code}
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode"]
            }
        }
    }
}, solc_version="0.8.0")

# Extract
contract = compiled_sol["contracts"]["AccessControlLogs.sol"]["AccessControlLogs"]
abi = contract["abi"]
bytecode = contract["evm"]["bytecode"]["object"]

# Save ABI
Path("blockchain/AccessControlLogs.abi.json").write_text(json.dumps(abi, indent=2))
Path("blockchain/AccessControlLogs.bytecode").write_text(bytecode)

print("✅ Compilation successful.")
