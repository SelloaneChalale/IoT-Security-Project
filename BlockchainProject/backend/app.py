from flask import Flask, jsonify, request
from web3 import Web3
import json

app = Flask(__name__)

# Initialize Web3 connection
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

# Load contract ABI and bytecode
artifacts_path = 'C:/Users/PC/IoT_Security_Project/BlockchainProject/artifacts/contracts/IoTData.sol/IoTData.json'
with open(artifacts_path) as artifacts_file:
    artifacts = json.load(artifacts_file)
abi = artifacts['abi']
bytecode = artifacts['bytecode']

# Set the contract address
contract_address = "0x5fbdb2315678afecb367f032d93f642f64180aa3".strip()
contract_address_checksum = w3.to_checksum_address(contract_address)

# Initialize contract instance
contract = w3.eth.contract(address=contract_address_checksum, abi=abi)

device_id = "0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266"
checksum_device_id = Web3.to_checksum_address(device_id)

# Route to authorize a device
@app.route('/authorizeDevice', methods=['POST'])
def authorize_device():
    tx_hash = contract.functions.registerDevice(checksum_device_id).transact({'from': w3.eth.accounts[0]})
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return jsonify({'status': 'Device registered', 'tx_hash': tx_hash.hex()}), 200

# Route to log data
@app.route('/logData', methods=['POST'])
def log_data():
    data = request.json
    if 'value' not in data:
        return jsonify({'error': 'Data value is required'}), 400
    try:
        data_hash = w3.solidity_keccak(['string'], [data['value']])
        tx_hash = contract.functions.storeData(data_hash).transact({'from': w3.eth.accounts[0]})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({'status': 'Data logged', 'tx_hash': tx_hash.hex()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to retrieve data based on its hash
@app.route('/retrieveData', methods=['POST'])
def retrieve_data():
    data = request.json
    if 'data_hash' not in data:
        return jsonify({'error': 'Data hash is required'}), 400
    try:
        data_hash = w3.to_bytes(hexstr=data['data_hash'])
        device, timestamp = contract.functions.storedData(data_hash).call()
        return jsonify({'device': device, 'timestamp': timestamp}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to retrieve all data hashes
@app.route('/getAllDataHashes', methods=['GET'])
def get_all_data_hashes():
    try:
        all_data_hashes = contract.functions.getAllDataHashes().call()
        data_hashes_hex = [w3.to_hex(data_hash) for data_hash in all_data_hashes]
        return jsonify({'data_hashes': data_hashes_hex}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to verify if a device is authorized
@app.route('/verifyDevice', methods=['POST'])
def verify_device():
    device_id = request.json.get('device_id')
    if not device_id:
        return jsonify({'error': 'Device ID is required'}), 400
    
    try:
        checksum_device_id = Web3.to_checksum_address(device_id)
        is_verified = contract.functions.authorizedDevices(checksum_device_id).call()
        return jsonify({'verified': is_verified}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to log an attack
@app.route('/logAttack', methods=['POST'])
def log_attack():
    data = request.json
    if 'attackType' not in data or 'threatLevel' not in data:
        return jsonify({'error': 'Both attackType and threatLevel are required'}), 400
    try:
        attack_type = data['attackType']
        threat_level = data['threatLevel']
        tx_hash = contract.functions.logAttack(attack_type, threat_level).transact({'from': w3.eth.accounts[0]})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({'status': 'Attack logged', 'tx_hash': tx_hash.hex()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
