# IoT-Security-Project
Blockchain

### Prerequisites

- [Node.js](https://nodejs.org/en/download/)
- [Python](https://www.python.org/downloads/)

Note: _Windows Build Tools is required to install web3. Install through Powershell(Admin) if not installed already_

```bash
npm install -g windows-build-tools
```
### Steps

Firstly, you need to compile the smart contract and start a local blockchain. Follow the steps below to do so:

1. Install required dependencies:

```bash
npm install
```

2. Start a local blockchain using Hardhat:

```bash
npx hardhat node
```

3. Compile contract in a separate terminal:

```bash
npx hardhat compile
```

4. Install python dependencies and interact with API Endpoints

```bash
pip install -r requirements.txt

python app.py

#authorisedevice
Invoke-RestMethod -Uri "http://localhost:5000/authorizeDevice" -Method Post -ContentType "application/json" -Body (@{ device_id = "device123" } | ConvertTo-Json)

#logdata
Invoke-RestMethod -Uri "http://localhost:5000/logData" -Method Post -ContentType "application/json" -Body (@{ value = "sensor_data_value_here" } | ConvertTo-Json)

#retrievedata
Invoke-RestMethod -Uri "http://localhost:5000/retrieveData" -Method Post -ContentType "application/json" -Body (@{ data_hash = "0xf87fd4a9b155bfff1c4e543e88032db1fa43d0f165b96401e9f15116ac58919d" } | ConvertTo-Json)

#verifydevice
Invoke-RestMethod -Uri "http://localhost:5000/verifyDevice" -Method Post -ContentType "application/json" -Body (@{ device_id = "0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266" } | ConvertTo-Json)

#getalldatahashes
Invoke-RestMethod -Uri "http://127.0.0.1:5000/getAllDataHashes" -Method GET

#authorisedevice
Invoke-RestMethod -Uri "http://127.0.0.1:5000/authorizeDevice" -Method POST -Headers @{ "Content-Type"="application/json" }


## Built With

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used for the backend
- [Web3.py](https://web3py.readthedocs.io/en/stable/) - Python library for interacting with Ethereum blockchain
- [Hardhat](https://hardhat.org/) - Ethereum development environment for compiling, testing, deploying, and interacting with smart contracts
- [Solidity](https://docs.soliditylang.org/en/v0.8.4/) - Ethereum's smart contract programming language
