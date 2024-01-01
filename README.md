## What this repo contains:
This repository includes code that interacts with the Ethereum network, 
providing examples of fetching events from Aave DeFi smart contracts and
aggregating the collected liquidation rewards. 

For example python/main.py<br>
contains example how to fetch events from AAVE LiquidationCall smart contract
starting from Nov-19-2021 (block 13646063).<br>

The purpose of this repository is to explore Ethereum network and smart contracts architecture 
while assessing the profitability of Aave's platform liquidation

## Liquidator bot for Aave crypto liquiduty protocol
In the context of decentralized finance (DeFi) and lending platforms like Aave, "liquidation" <br>
typically refers to the process of seizing and selling collateral to repay a loan when the borrower's position falls below a certain threshold,<br>
known as the liquidation threshold. </br>

Here's a basic overview of how liquidation works on platforms like Aave:</br>

## Borrowing with Collateral: 
When users borrow funds on Aave, they must provide collateral in the form of other cryptocurrencies.</br>
The collateral serves as security for the loan.

## Liquidation Threshold:
Aave sets a liquidation threshold for each asset. </br>
If the value of the collateral falls below this threshold due to market fluctuations, the position becomes vulnerable to liquidation.</br>

## Liquidation Process: 
If the collateralized position approaches or falls below the liquidation threshold,</br>
the Aave protocol may automatically liquidate a portion of the collateral to repay the outstanding loan. </br>
This involves selling the borrower's collateral on the open market.</br>

## Liquidation Incentives: 
To encourage users to monitor and maintain their collateralized positions, </br>
Aave often includes an incentive mechanism. </br>
Those who identify and liquidate risky positions may receive a portion of the liquidated collateral as a reward. </br>

## Auction Mechanism: 
In some cases, the liquidation process involves an auction where other users can bid for the collateral being sold. </br>
This auction mechanism helps to ensure a fair market price for the liquidated assets. </br>

## Useful Links </br>
Fast intro in Ethereum infra (very useful) is here: https://ethereum.org/en/whitepaper/<br />
An intro to Ethereum infra is here: https://ethereum.org/en/developers/docs/intro-to-ethereum/<br />
Here is the main site: https://aave.com/ where crypto assets and its borrow/deposits rates can be found<br />
Developer portal is here: https://docs.aave.com/developers/<br />
Aave liquidation protocol is here: https://docs.aave.com/developers/guides/liquidations<br />
AAve liqidation FAQ us here: https://docs.aave.com/faq/liquidations<br />
An explanation about Aave liqudation process is here: https://medium.com/coinmonks/creating-a-liquidation-script-for-aave-defi-protocol-ef584ad87e8f<br />
Aave flash loans an explanation is here: https://medium.com/aave/sneak-peek-at-flash-loans-f2b28a394d62<br />
Etherium Full Stack env set up is here: https://www.freecodecamp.org/news/full-stack-ethereum-development/<br />
