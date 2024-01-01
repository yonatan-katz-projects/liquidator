import json
import datetime
import pandas as pd
from web3 import Web3
from web3._utils.abi import get_constructor_abi, merge_args_and_kwargs
from web3._utils.events import get_event_data
from web3._utils.filters import construct_event_filter_params
from web3._utils.contracts import encode_abi

from reserve_asset import get_crypto_asset_usd_price
from reserve_asset import split_user_loan_deposit_bitmask
from reserve_asset import split_asset_config_bitmask
from reserve_asset import CRYPTO_ASSET_ADDRESS_TO_NAME
from reserve_asset import convert_addr_in_crypto_asset
from crypto_utils import convert_wei_to_eth
from crypto_utils import convert_decimal_to_float

from config import *

START_BLOCK_FOR_EVENT_FETCHING = 13646063

'''Parse Borrowd event based on AAVE V1 protocol:
   https://docs.aave.com/developers/v/1.0/developing-on-aave/the-protocol/lendingpool#borrow-1
'''
def handle_borrow_event_V1(event_data):
    collateral_crypto_address = event_data['_reserve']
    crypto_collatera_asset = convert_addr_in_crypto_asset(collateral_crypto_address)

    #TODO: convert Wei to USD
    user_who_borrowed_address = event_data['_user']
    amount = event_data['_amount'] #amount borrowed, in Wei!
    borrow_rate_mode = event_data['_borrowRateMode']
    borrow_rate = event_data['_borrowRate'] #1-Fixed, 2-Float
    origination_fee = event_data['_originationFee']
    borrow_balance_increase = event_data['_borrowBalanceIncrease'] #in Wei!
    timestamp = event_data['_timestamp']
    datetime_time = datetime.datetime.fromtimestamp(timestamp)

    print('Borrow \n'
          'collateral_asset:{}, borrowed_amount(ETH):{}, balance_increase(ETH):{}, borrow_rate_mode:{}\n'
          'user:{}, datetime_time:{}, '.
          format(crypto_collatera_asset,
                 convert_wei_to_eth(amount),
                 convert_wei_to_eth(borrow_balance_increase),
                 borrow_rate_mode,
                 user_who_borrowed_address,
                 datetime_time))


def handle_borrow_event_V2(event_data):
    collateral_crypto_address = event_data['reserve']
    crypto_collatera_asset = 'not_known'
    if collateral_crypto_address in CRYPTO_ASSET_ADDRESS_TO_NAME.keys():
        crypto_collatera_asset = CRYPTO_ASSET_ADDRESS_TO_NAME[collateral_crypto_address]

    #TODO: convert Wei to USD
    on_BehalfOf_borrowed_address = event_data['onBehalfOf']
    user_who_borrowed_address = event_data['user']
    amount = event_data['amount'] #amount borrowed, in Wei!
    borrow_rate_mode = event_data['borrowRateMode']
    borrow_rate = event_data['borrowRate'] #1-Fixed, 2-Float
    referral = event_data['referral']


    print('Borrow \n'
          'collateral_asset:{}, borrowed_amount(ETH):{}, borrow_rate_mode:{}\n'
          'user:{}, on_BehalfOf:{}'.
          format(crypto_collatera_asset,
                 convert_wei_to_eth(amount),
                 borrow_rate_mode,
                 user_who_borrowed_address,
                 on_BehalfOf_borrowed_address))

    return convert_wei_to_eth(amount)


def handle_liqudation_call_event_V2(event_data, err_handler):
    collateralAsset = event_data['collateralAsset']
    debtAsset = event_data['debtAsset']
    user = event_data['user']
    debtToCover = event_data['debtToCover']
    liquidatedCollateralAmount = event_data['liquidatedCollateralAmount']
    liquidator = event_data['liquidator']
    receiveAToken = event_data['receiveAToken']

    collateralAsset_name = convert_addr_in_crypto_asset(collateralAsset)
    debtAsset_name  = convert_addr_in_crypto_asset(debtAsset)
    debtToCover = convert_decimal_to_float(debtAsset_name, debtToCover)
    liquidatedCollateralAmount = convert_decimal_to_float(collateralAsset_name, liquidatedCollateralAmount)

    if (collateralAsset_name=='not_know') :
        if 'not_known_asset' in err_handler:
            err_handler['not_known_asset'].append(collateralAsset)
        else:
            err_handler['not_known_asset'] = [collateralAsset]

    print("Raw message:{}\n".format(event_data))

    print("LiquidationCall\n"
          "collateralAsset_name:{}"
          ",debtAsset_name:{}"
          ",debtToCover:{}"
          ",liquidatedCollateralAmount:{}"
          ",user:{},liquidator:{}".
          format(collateralAsset_name, debtAsset_name, debtToCover,
                 liquidatedCollateralAmount, user, liquidator))

    return {'received':[collateralAsset_name, liquidatedCollateralAmount], 'paid':[debtAsset_name, debtToCover], 'liquidator':liquidator, 'user':user}

'''Based on: https://github.com/aave/protocol-v2/blob/ice/mainnet-deployment-03-12-2020/contracts/interfaces/ILendingPool.sol
'''
def fetch_events(type):
    web3 = Web3(Web3.HTTPProvider(Infura_EndPoint))
    from_block = START_BLOCK_FOR_EVENT_FETCHING
    to_block = 'latest'
    address = None
    topics = None

    contract = web3.eth.contract(address=Lending_Pool_V2_Address, abi=Lending_Pool_V2_ABI)
    if type == 'Borrow':
        event = contract.events.Borrow
    elif type == 'LiquidationCall':
        event = contract.events.LiquidationCall
    elif type == 'FlashLoan':
        event = contract.events.FlashLoan
    else:
        raise Exception('Not supported event type!')

    abi = event._get_event_abi()
    abi_codec = event.web3.codec


    # Set up any indexed event filters if needed
    argument_filters = dict()
    _filters = dict(**argument_filters)

    data_filter_set, event_filter_params = construct_event_filter_params(
        abi,
        abi_codec,
        contract_address=event.address,
        argument_filters=_filters,
        fromBlock=from_block,
        toBlock=to_block,
        address=address,
        topics=topics,
    )

    # Call node over JSON-RPC API
    logs = event.web3.eth.getLogs(event_filter_params)

    # Convert raw binary event data to easily manipulable Python objects
    err_handler = {}
    transactions = set()
    Transaction = []
    Balance = []
    Liquidator = []
    DebtAsset = []
    DebtAmountCovered = []
    ColAsset = []
    ColAmountCollected = []
    User = []
    Block = []
    for entry in logs:
        data = dict(get_event_data(abi_codec, abi, entry))

        block_number = data['blockNumber']
        address = data['address'] #Lending Pool Contract address
        transaction_hash = data['transactionHash'].hex()

        '''Avoid having handle transaction multiple times'''
        if transaction_hash not in transactions:
            transactions.add(transaction_hash)

            print('##### block_number:{}, transaction:{} #####\n'.format(block_number,transaction_hash))
            event_type = data['event']
            if event_type == 'Borrow':
                Block.append(block_number)
                ret = handle_borrow_event_V2(event_data=dict(data['args']))
            elif event_type == 'LiquidationCall':
                ret = handle_liqudation_call_event_V2(event_data=dict(data['args']), err_handler=err_handler)
                asset, amount = ret['received']
                received = amount * get_crypto_asset_usd_price(asset)
                ColAsset.append(asset)
                ColAmountCollected.append(amount)

                asset, amount = ret['paid']
                paid = amount * get_crypto_asset_usd_price(asset)
                DebtAsset.append(asset)
                DebtAmountCovered.append(amount)

                Transaction.append(transaction_hash)
                tx_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
                print(tx_receipt)

                '''Without Gas fee!'''
                Balance.append(received - paid)
                Liquidator.append(ret['liquidator'])
                User.append(ret['user'])
                Block.append(block_number)
            elif event_type == 'FlashLoan':
                Transaction.append(transaction_hash)
                pass

    if type == 'LiquidationCall':
        df = pd.DataFrame({'transaction': Transaction,
                           'balance': Balance,
                           'user': User,
                           'liquidator': Liquidator,
                           'col_asset': ColAsset,
                           'col_collected': ColAmountCollected,
                           'debt_asset': DebtAsset,
                           'debt_covered': DebtAmountCovered,
                           'block':Block})

    if type == 'FlashLoan':
        df = pd.DataFrame({'transaction': Transaction, 'block':Block})

    now = datetime.datetime.now()
    df.to_csv('{}/{}_{}.csv'.format(CACHE_FOLDER, type, now.strftime("%Y%m%d_%H%M%S")))

    pass



def call_getUserAccountData_V2(account='0x8d30e4b4C8D461d99Ee3FD67B3f7f0Ddaf9d3dD6'):
    web3 = Web3(Web3.HTTPProvider(Infura_EndPoint))
    contract = web3.eth.contract(address=Lending_Pool_V2_Address, abi=Lending_Pool_V2_ABI)

    '''Get assets index'''
    reserve_to_index = []
    ret = contract.functions.getReservesList().call()
    for i in range(len(ret)):
        print('reserved asset:',convert_addr_in_crypto_asset(ret[i]))
        reserve_to_index.append(ret[i])

    '''Get user asset config'''
    ret = contract.functions.getUserConfiguration(account).call()
    s = split_user_loan_deposit_bitmask(ret[0])
    for k in s.keys():
        is_col, is_borrowed = s[k]
        asset_addr = reserve_to_index[k]
        asset_name = convert_addr_in_crypto_asset(asset_addr)
        print('asset:{}, is_col:{}, is_borrowed:{}'.format(asset_name, is_col, is_borrowed))
    print('getUserConfiguration:{}'.format(ret))

    '''Get asset config'''
    for asset_addr in reserve_to_index:
        ret = contract.functions.getConfiguration(asset_addr).call()
        print("asset:{}, config:{}".format(convert_addr_in_crypto_asset(asset_addr), ret[0]))
        split_asset_config_bitmask(ret[0])
    ###
    ret = contract.functions.getUserAccountData(account).call()
    total_col_in_eth = convert_wei_to_eth(ret[0])
    total_debt_in_eth = convert_wei_to_eth(ret[1])
    available_borrows_in_eth = convert_wei_to_eth(ret[2])
    current_liquidation_threshold = ret[3]/100.0
    ltv = ret[4] /100.0
    healthFactor = ret[5]/1e18
    print('total_col_in_eth:{},total_debt_in_eth:{},available_borrows_in_eth:{},'
          'current_liquidation_threshold:{},ltv:{},healthFactor:{}'.
          format(total_col_in_eth,
                 total_debt_in_eth,
                 available_borrows_in_eth,
                 current_liquidation_threshold,
                 ltv,
                 healthFactor))
    pass



if __name__ == '__main__':
    #fetch_events()
    call_getUserAccountData_V2()
