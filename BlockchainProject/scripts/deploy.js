const { ethers } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners(); // Use ethers.getSigners() directly
    console.log("Deploying contracts with the account:", deployer.address);

    // Deploy the IoTData contract
    const IoTData = await ethers.getContractFactory("IoTData");
    const iotDataContract = await IoTData.deploy();
    // await iotDataContract.deployed(); // Wait for the deployment to be mined

    console.log("IoTData contract deployed at:", iotDataContract.address); // Use address directly
}

// Run the deployment script
main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error("Error in script execution:", error);
        process.exit(1);
    });
