# AI-ZTB Framework for EV Charging Security Simulation

This project implements a simulation of an AI-driven Zero Trust Blockchain (ZTB-AI) framework for secure and auditable access control in Electric Vehicle (EV) charging infrastructure. The framework integrates IAM (authentication/authorization), AI-based risk scoring, blockchain logging, and IPFS for decentralized audit logs.

## Structure
- `ai_engine/`: AI risk scoring and model code
- `blockchain/`: Smart contracts, blockchain API, and IPFS integration
- `iam/`: Authentication and policy engine
- `simulation/`: Synthetic log generation, attack scenarios, evaluation scripts
- `config/`: System configuration
- `test/`: Unit and integration tests
- `app.py`: Main entry point

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Generate synthetic logs: `python simulation/generate_logs.py`
3. Train AI model: `python ai_engine/train_model.py`
4. **Compile and deploy blockchain contract automatically:**
   - Ensure Ganache GUI is running (see below)
   - Ensure `solc` (Solidity compiler) is installed and in your PATH
   - Run: `python blockchain/compile_and_deploy.py`
   - This will compile the contract, deploy it to Ganache, and update the contract address in `blockchain_api.py` automatically.
5. Run simulation: `python simulation/scenario_runner.py`
6. Plot results: `python simulation/graph_plotter.py`

### Ganache Setup
- Launch Ganache GUI and ensure the RPC server is running at `http://127.0.0.1:8545` (default)
- Use the first account as the deployer (shown in GUI)

### Solidity Compiler (solc)
- Install from https://docs.soliditylang.org/en/latest/installing-solidity.html
- Or use npm: `npm install -g solc`

### IPFS Setup
- Install IPFS from https://docs.ipfs.tech/install/
- Start the IPFS daemon: `ipfs daemon`
- Ensure it runs at default address (`127.0.0.1:5001`)

### Troubleshooting
- If `blockchain/compile_and_deploy.py` fails, check:
  - Ganache GUI is running and not blocked by firewall
  - `solc` is installed and available in your terminal
  - IPFS daemon is running for log storage
- If you update the smart contract, always rerun `compile_and_deploy.py` to refresh the ABI and address

See the full documentation for details.
