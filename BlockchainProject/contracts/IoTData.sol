// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.27;

contract IoTData {
    address public owner;
    mapping(address => bool) public authorizedDevices;
    mapping(address => uint) public lastDataTransmissionTime;
    bytes32[] public allDataHashes;

    // Struct to store data information
    struct Data {
        address device;
        uint timestamp;
    }

    mapping(bytes32 => Data) public storedData;

    // Struct to store attack information
    struct Attack {
        string attackType;
        uint threatLevel;
        uint timestamp;
    }

    // Mapping to store attacks by device address
    mapping(address => Attack[]) public deviceAttacks;

    // Events
    event DeviceRegistered(address device);
    event DeviceDeauthorized(address device);
    event DataStored(address device, bytes32 dataHash, uint timestamp);
    event AttackLogged(address device, string attackType, uint threatLevel, uint timestamp);

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner.");
        _;
    }

    modifier onlyAuthorizedDevice() {
        require(authorizedDevices[msg.sender], "Device not authorized.");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    // Function to register a device
    function registerDevice(address _device) public onlyOwner {
        require(!authorizedDevices[_device], "Device already registered.");
        authorizedDevices[_device] = true;
        emit DeviceRegistered(_device);
    }

    // Function to deauthorize a device
    function deauthorizeDevice(address _device) public onlyOwner {
        require(authorizedDevices[_device], "Device not registered: address not found.");
        authorizedDevices[_device] = false; 
        emit DeviceDeauthorized(_device);
    }

    // Function for authorized devices to store data
    function storeData(bytes32 dataHash) public onlyAuthorizedDevice {
        require(storedData[dataHash].device == address(0), "Data already exists: hash collision.");
        storedData[dataHash] = Data(msg.sender, block.timestamp);
        lastDataTransmissionTime[msg.sender] = block.timestamp;
        
        // Add to the array of all data hashes
        allDataHashes.push(dataHash);

        emit DataStored(msg.sender, dataHash, block.timestamp);
    }

    // Function to get all stored data hashes
    function getAllDataHashes() public view returns (bytes32[] memory) {
        return allDataHashes;
    }

    // Function to check if data exists
    function checkDataExists(bytes32 dataHash) public view returns (bool) {
        return storedData[dataHash].device != address(0);
    }

    function getData(bytes32 dataHash) public view returns (address device, uint timestamp) {
        require(storedData[dataHash].device != address(0), "No data found for this hash.");
        Data memory data = storedData[dataHash];
        return (data.device, data.timestamp);
    }

    // Function to register multiple devices
    function registerMultipleDevices(address[] memory _devices) public onlyOwner {
        for (uint i = 0; i < _devices.length; i++) {
            if (!authorizedDevices[_devices[i]]) {
                authorizedDevices[_devices[i]] = true;
                emit DeviceRegistered(_devices[i]);
            }
        }
    }

    // Function to log attacks
    function logAttack(string memory attackType, uint threatLevel) public onlyAuthorizedDevice {
        // Record the attack in the device's attack history
        Attack memory newAttack = Attack({
            attackType: attackType,
            threatLevel: threatLevel,
            timestamp: block.timestamp
        });
        
        deviceAttacks[msg.sender].push(newAttack);

        // Emit an event with the attack information
        emit AttackLogged(msg.sender, attackType, threatLevel, block.timestamp);
    }

    // Function to get the attack history of a device
    function getDeviceAttacks(address device) public view returns (Attack[] memory) {
        return deviceAttacks[device];
    }
}

