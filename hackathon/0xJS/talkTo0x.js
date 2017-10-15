const Web3 = require('web3');
const ZeroEx = require('0x.js').ZeroEx;
const BigNumber = require('bignumber.js');

const provider = new Web3.providers.HttpProvider('http://localhost:8545');

if (typeof web3 !== 'undefined') {
 web3 = new Web3(web3.currentProvider);
} else {
 // set the provider you want from Web3.providers
 web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'));
}

// Instantiate 0x.js instance
const zeroEx = new ZeroEx(provider);

(async () => {

	// Number of decimals to use (for ETH and ZRX)
	const DECIMALS = 18; 

	// Addresses
	const NULL_ADDRESS = ZeroEx.NULL_ADDRESS;                                    // Ethereum Null address
	//const WETH_ADDRESS = await zeroEx.etherToken.getContractAddressAsync();      // The wrapped ETH token contract
	//const ZRX_ADDRESS  = await zeroEx.exchange.getZRXTokenAddressAsync();        // The ZRX token contract
	//const EXCHANGE_ADDRESS   = await zeroEx.exchange.getContractAddressAsync();  // The Exchange.sol address (0x exchange smart contract)

	// deployed by hand
	//const WETH_ADDRESS = "0xe5767babd98915d1340358bbd1f305ce94786767" ;    
	//const ZRX_ADDRESS  = "0xf4025728e515290a7e691abd50bc8024bb6da8be";        
	//const EXCHANGE_ADDRESS = "0x3c08c02514b7b55cb32f06868ad0ecc8481c0f56";
	
	// deployed using truffle
	const WETH_ADDRESS = "0x06a49e79a8ea3be3d0aee6e09304a764cbfc7fb9" ;    
	const ZRX_ADDRESS  = "0x578c2529bae092745b35d638a8db6ad6877d4387"; 
	const EXCHANGE_ADDRESS = "0x229da43e4332d3dd83927e22f67eece38bc79408";
	
	var zrxtoken_abi = web3.eth.contract([{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"inputs":[],"payable":false,"type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]);

	var weth_abi = web3.eth.contract([{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"payable":true,"type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]);

	// Getting list of accounts
	//const accounts =  await zeroEx.getAvailableAddressesAsync();
	//console.log(accounts);
	//console.log(ZRX_ADDRESS);

	// Set our address
	//const [makerAddress, takerAddress] = accounts;
	
	makerAddress = web3.eth.accounts[0];
	takerAddress = web3.eth.accounts[1];
	
	console.log("maker: " + makerAddress);
	console.log("taker: " + takerAddress);
	console.log("zrxtoken contract total supply: " + zrxtoken_abi.at(ZRX_ADDRESS).totalSupply());
	console.log("maker balance: " + web3.eth.getBalance(makerAddress));
		
	// Unlimited allowances to 0x contract for maker and taker
	const txHashAllowMaker = await zeroEx.token.setUnlimitedProxyAllowanceAsync(ZRX_ADDRESS,  makerAddress);
	await zeroEx.awaitTransactionMinedAsync(txHashAllowMaker);
	console.log('Maker Allowance Mined...');

	const txHashAllowTaker = await zeroEx.token.setUnlimitedProxyAllowanceAsync(WETH_ADDRESS, takerAddress);
	await zeroEx.awaitTransactionMinedAsync(txHashAllowTaker);
	console.log('takerFee Allowance Mined...');

	// Deposit WETH
	const ethToConvert = ZeroEx.toBaseUnitAmount(new BigNumber(1), DECIMALS); // Number of ETH to convert to WETH

	const txHashWETH = await zeroEx.etherToken.depositAsync(ethToConvert, takerAddress);
	await zeroEx.awaitTransactionMinedAsync(txHashWETH);
	console.log('ETH -> WETH Mined...');

	// Generate order
	const order = { 
			 maker: makerAddress, 
			 taker: NULL_ADDRESS,
	           	 feeRecipient: NULL_ADDRESS,
	           	 makerTokenAddress: ZRX_ADDRESS,
	              	 takerTokenAddress: WETH_ADDRESS,
	              	 exchangeContractAddress: EXCHANGE_ADDRESS,
	              	 salt: ZeroEx.generatePseudoRandomSalt(),
	           	 makerFee: new BigNumber(0),
	              	 takerFee: new BigNumber(0),
	            	 makerTokenAmount: ZeroEx.toBaseUnitAmount(new BigNumber(0.2), DECIMALS),  // Base 18 decimals
	           	 takerTokenAmount: ZeroEx.toBaseUnitAmount(new BigNumber(0.3), DECIMALS),  // Base 18 decimals
	           	 expirationUnixTimestampSec: new BigNumber(Date.now() + 3600000),          // Valid up to an hour
	              };

	// Create orderHash
	const orderHash = ZeroEx.getOrderHashHex(order);

	// Signing orderHash -> ecSignature
	const ecSignature = await zeroEx.signOrderHashAsync(orderHash, makerAddress);
	
	console.log("Valid ecSignature: " + ecSignature);

	// Appending signature to order
	const signedOrder = { 
			       ...order, 
			       ecSignature, 
	                    };
	                    
	console.log("Signed order: " + JSON.stringify(signedOrder));

	// Verify if order is fillable
	//await zeroEx.exchange.validateOrderFillableOrThrowAsync(signedOrder);
	
	//console.log("Order validated as fillable");

	// Try to fill order
	//const shouldThrowOnInsufficientBalanceOrAllowance = true;
	//const fillTakerTokenAmount = ZeroEx.toBaseUnitAmount(new BigNumber(0.1), DECIMALS);

	// Try filling order
	//const txHash = await zeroEx.exchange.fillOrderAsync(signedOrder, fillTakerTokenAmount, 
    //                                                        shouldThrowOnInsufficientBalanceOrAllowance, takerAddress,);
                                                      
	// Transaction Receipt
	//const txReceipt = await zeroEx.awaitTransactionMinedAsync(txHash);
	//console.log(txReceipt.logs);

})().catch(function(e)
{
	console.log("Error: " + JSON.stringify(e));
});