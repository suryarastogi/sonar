I've encountered several problems trying to write a JS script that would set allowances and then sign an order json. 

First of all, the test rpc set up didn't work out of the box as explained in the tutorial. Having tried several fixes that didn't work I decided to deploy 0x contracts on my own private network. I did that using truffle and the 0x migration contracts. 

As a result I deployed all the contracts and could hard code their addresses. Addresses of contracts of particular ERC20 tokens can be looked up in token registry.

The JS script from the tutorial didn't work though so I dug into the 0x code and found two problems with it.

One was that the promise-based lookups of contract addresses and instances didn't work and promises were never fulfilled. I identified all such promises and replaced them with the contract addresses and instances needed.

Second problem was to do with order signature. There is a check whether parity or testrpc nodes are running because those add personal prefix themselves before hashing order. For other node types that had to be done manually. I was running a private node in rpc mode which was incorrectly classified as neither parity nor testrpc and the order signature was calculated incorrectly. Fixing that (0x.js file) generated a correct signature.

The order json generated could be published on the front end, for example as a pop-up on clicking on particular exchange rates. A further enhancement would be to make a click automatically submit a transaction that fills the order (using MetaMask).