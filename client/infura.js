const LendingPoolV2Artifact = require("@aave/protocol-v2/artifacts/contracts/protocol/lendingpool/LendingPool.sol/LendingPool.json");

const abi = require("./abi.js");
const chainlink = require("./chainlink.js");

const { ethers } = require("ethers");

const uniswap_anchored_view_address =
  "0x6D2299C48a8dD07a872FDd0F8233924872Ad1071";

const aave_lending_pool_v2_abi = LendingPoolV2Artifact.abi;
const aave_lending_pool_v2_address =
  "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9";

const aave_incentive_controller_address =
  "0xd784927Ff2f95ba542BfC824c8a8a98F3495f6b5";

const chainlink_aggregator_address_eth_usd =
  "0x37bC7498f4FF12C19678ee8fE19d713b87F6a9e6";

//const projectId = "fd3ac79f46ba4500be8e92da9632b476"; //Yonatan
const projectId = "474dfacad06547a4aba817b93fa852c9";

//
// Timestamp signature
//
const tstamp = () => new Date(Date.now()).toISOString();

//
// Conversion from BigNumber to floating point values
//
const toPrice = (big_number, coin_pair) => {
  if (coin_pair.includes("/USD")) {
    const denom = 1e8;
    return ethers.BigNumber.from(big_number).toNumber() / denom;
  }
  return ethers.utils.formatEther(big_number.toString());
};

//
//Load accounts from json file
//
const loadAccounts = (json_file) => {
  console.log("loading tracked accounts from %s", json_file);
  var accounts = require(json_file);

  console.log("tracked accounts:");
  for (account of accounts) {
    account.health_factor = 0;
    account.totalCollateralETH = 0;
    account.totalDebtETH = 0;
    account.currentLiquidationThreshold = 0;

    console.log(
      "%s collateral:%s debt:%s",
      account.account,
      account.collateralAssets,
      account.debtAssets
    );
  }

  return accounts;
};

//
//Locally calculated health factor
//
const hFactor = (account) => {
  return (
    (account.totalCollateralETH * account.currentLiquidationThreshold) /
    account.totalDebtETH
  );
};

//
//Fetch account health
//
const fetchAccountState = async (account, aave_lending_pool_contract) => {
  const account_data = await aave_lending_pool_contract.getUserAccountData(
    account.account
  );

  var prev_health_factor = account.health_factor;

  account.health_factor = ethers.utils.formatEther(account_data.healthFactor);
  account.totalCollateralETH = ethers.utils.formatEther(
    account_data.totalCollateralETH
  );
  account.totalDebtETH = ethers.utils.formatEther(account_data.totalDebtETH);
  account.currentLiquidationThreshold =
    ethers.BigNumber.from(account_data.currentLiquidationThreshold).toNumber() /
    1e4;

  console.log(
    "%s %s health factor: %s %s %s (%f)",
    tstamp(),
    account.account,
    account.collateralAssets,
    account.debtAssets,
    account.health_factor,
    account.health_factor - prev_health_factor
  );
};

//
//Fetch accounts by coin pair and query their health
//
const fetchAccountsStateByCoinPair = async (
  accounts,
  coin_pair,
  aave_lending_pool_contract
) => {
  if (!coin_pair.includes("/ETH")) {
    //ignore none ETH based currencies
    return;
  }

  const coin = coin_pair.split("/")[0];
  for (account of accounts) {
    if (
      account.collateralAssets.includes(coin) ||
      account.debtAssets.includes(coin)
    ) {
      await fetchAccountState(account, aave_lending_pool_contract);
    }
  }
};

//
//Top N accounts - i.e. accounts with lowest health factor
//
const topNAccounts = (accounts, N) => {
  accounts.sort((a, b) => {
    return a.health_factor - b.health_factor;
  });

  return accounts.slice(0, N);
};

//
//Main
//
async function main() {
  const tracked_accounts_file = process.argv[2];
  if (!tracked_accounts_file) {
    console.log("missing argument - tracked files json file");
    return;
  }

  //Running modes
  const fast_init = false;
  const test_mode = false;
  const monitor_blocks = false;
  const monitor_pending_tx = false;

  //Load tracked accounts
  var tracked_accounts = loadAccounts(tracked_accounts_file);

  console.log("%s running infura client", tstamp());
  provider = ethers.providers.InfuraProvider.getWebSocketProvider(
    "homestead",
    projectId
  );

  block_number = await provider.getBlockNumber();
  console.log("%s connected to infura, last block %d", tstamp(), block_number);

  //
  //AAVE lending pool contract
  //
  const aave_lending_pool_contract = new ethers.Contract(
    aave_lending_pool_v2_address,
    aave_lending_pool_v2_abi,
    provider
  );

  //
  //Fetch current accounts state
  //
  if (!fast_init) {
    for (account of tracked_accounts) {
      await fetchAccountState(account, aave_lending_pool_contract);
    }
  }

  if (test_mode) {
    await fetchAccountsStateByCoinPair(
      tracked_accounts,
      "AAVE/ETH",
      aave_lending_pool_contract
    );
  }

  /* await aave_lending_pool_contract.connect(provider);
     * aave_lending_pool_contract.on("Borrow", (...evt) => {
     *   console.log("%s lending pool borrow %s", tstamp(), evt);
     * });

     * aave_lending_pool_contract.on("Deposit", (...evt) => {
     *   console.log("%s lending pool deposit %s", tstamp(), evt);
     * }); */

  aave_lending_pool_contract.on("LiquidationCall", (...evt) => {
    console.log("%s lending pool liquidation  %s", tstamp(), evt);
    for (const _e of evt) {
      console.log("%s", _e);
    }
  });

  /* aave_lending_pool_contract.on("FlashLoan", (...evt) => {
   *   console.log("%s lending pool flashloan  %s", tstamp(), evt);
   *   for (const _e of evt) {
   *     console.log("%s", _e);
   *   }
   * }); */

  /* aave_lending_pool_contract.on("Repay", (...evt) => {
   *   console.log("%s lending pool repay  %s", tstamp(), evt);
   * }); */

  //
  //Price feed contract - uniswap
  //
  const price_feed_contract = new ethers.Contract(
    uniswap_anchored_view_address,
    abi.uniswap_anchored_view_abi,
    provider
  );

  await price_feed_contract.connect(provider);

  const symbol_map = {};
  for (const symbol of [
    "ETH",
    "BTC",
    "DAI",
    "LINK",
    "USDT",
    "AAVE",
    "UNI",
    "YFI",
    "COMP",
    "MKR",
    "SUSHI",
    "USDC",
  ]) {
    const config = await price_feed_contract.getTokenConfigBySymbol(symbol);
    symbol_map[config["symbolHash"]] = symbol;

    if (!fast_init) {
      const price = await price_feed_contract.price(symbol);
      console.log(
        "%s, %s/USD price: %s",
        tstamp(),
        symbol,
        price.toNumber() / 1e6
      );
    }
  }

  price_feed_contract.on("PriceUpdated", (...evt) => {
    const symbol = symbol_map[evt[0]];
    if (typeof symbol !== "undefined") {
      console.log(
        "%s %d uniswap update  - price %s/USD %f",
        tstamp(),
        evt[2]["blockNumber"],
        symbol,
        evt[1].toNumber() / 1e6
      );
    }
  });

  //
  //Chainlink price oracles
  //
  const chainlink_oracles = {};
  for (const [contract, coin_pair] of Object.entries(chainlink.price_oracles)) {
    const oracle = new ethers.Contract(contract, abi.chainlink_abi, provider);

    oracle.on("AnswerUpdated", (...evt) => {
      var price = toPrice(evt[0], coin_pair);
      console.log(
        "%s %s chainlink price update %s %f",
        tstamp(),
        evt[3]["blockNumber"],
        coin_pair,
        price
      );

      //Recalc accounts health for accounts that hold this coin
      fetchAccountsStateByCoinPair(
        tracked_accounts,
        coin_pair,
        aave_lending_pool_contract
      );
    });

    chainlink_oracles[coin_pair] = oracle;

    if (!fast_init) {
      const latest_answer = await oracle.latestAnswer();
      console.log(
        "%s registering chainlink price oracle %s %s",
        tstamp(),
        coin_pair,
        toPrice(latest_answer, coin_pair)
      );
    }
  }

  //'special' contract eth/usd price
  const chainlink_eth_usd_contract = new ethers.Contract(
    chainlink_aggregator_address_eth_usd,
    abi.chainlink_abi,
    provider
  );

  //
  // Register for pending transactions
  //
  if (monitor_pending_tx) {
    provider.on("pending", (tx) => {
      //console.log("%s pending tx: %s", tstamp(), tx);
      /* provider.getTransaction(tx).then(function (transaction) {
	 console.log(transaction); 
       *    }); */
    });
  }

  if (monitor_blocks) {
    provider.on("block", (tx) => {
      console.log("%s block: %s", tstamp(), tx);
    });
  }

  console.log("%s begin listening to live events", tstamp());

  while (true) {
    //Periodiclly track eth price via chainlink contract
    var eth_usd_price = await chainlink_eth_usd_contract.latestAnswer();
    eth_usd_price = eth_usd_price.toNumber() / 1e8;
    block_number = await provider.getBlockNumber();
    console.log(
      "%s %d chainlink query eth/usd price: %f",
      tstamp(),
      block_number,
      eth_usd_price
    );

    //Sleep for a while - listening to events in background
    const MIN = 60000;
    await new Promise((res) => setTimeout(() => res(null), 5 * MIN));

    //Query state of top N accounts i.e. nearest liquidation
    const top_n = topNAccounts(tracked_accounts, 10);
    for (account of top_n) {
      await fetchAccountState(account, aave_lending_pool_contract);
    }
  }
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
