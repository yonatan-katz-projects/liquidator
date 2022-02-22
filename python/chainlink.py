import config
import pandas as pd
import numpy as np
from web3 import Web3
from ens import ENS
from web3._utils.filters import construct_event_filter_params
'''Update rule:
    https://docs.chain.link/docs/faq/
    https://ethereum.stackexchange.com/questions/112408/how-often-are-chainlink-price-feeds-updated
    https://data.chain.link/ethereum/mainnet/crypto-usd/eth-usd
    https://docs.chain.link/docs/feed-registry/
    https://en.wikipedia.org/wiki/ISO_4217
    https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/interfaces/FeedRegistryInterface.sol
'''

'''See from: https://docs.chain.link/docs/ethereum-addresses/
      or https://data.chain.link/
'''
CHAIN_LINK_ADDR = {
    'ETH': {'USD': Web3.toChecksumAddress('0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419')},
}

ETH_addr = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

CHAIN_LINK_FEED_REG_ADDR = "0x47Fb2585D2C56Fe188D0E6ec628a38b74fCeeeDf"
CHAIN_LINK_FEED_REG_ABI='[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accessController","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"AccessControllerSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"asset","type":"address"},{"indexed":true,"internalType":"address","name":"denomination","type":"address"},{"indexed":true,"internalType":"address","name":"latestAggregator","type":"address"},{"indexed":false,"internalType":"address","name":"previousAggregator","type":"address"},{"indexed":false,"internalType":"uint16","name":"nextPhaseId","type":"uint16"},{"indexed":false,"internalType":"address","name":"sender","type":"address"}],"name":"FeedConfirmed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"asset","type":"address"},{"indexed":true,"internalType":"address","name":"denomination","type":"address"},{"indexed":true,"internalType":"address","name":"proposedAggregator","type":"address"},{"indexed":false,"internalType":"address","name":"currentAggregator","type":"address"},{"indexed":false,"internalType":"address","name":"sender","type":"address"}],"name":"FeedProposed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"address","name":"aggregator","type":"address"}],"name":"confirmFeed","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAccessController","outputs":[{"internalType":"contract AccessControllerInterface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"uint256","name":"roundId","type":"uint256"}],"name":"getAnswer","outputs":[{"internalType":"int256","name":"answer","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"getCurrentPhaseId","outputs":[{"internalType":"uint16","name":"currentPhaseId","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"getFeed","outputs":[{"internalType":"contract AggregatorV2V3Interface","name":"aggregator","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"uint80","name":"roundId","type":"uint80"}],"name":"getNextRoundId","outputs":[{"internalType":"uint80","name":"nextRoundId","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"uint16","name":"phaseId","type":"uint16"}],"name":"getPhase","outputs":[{"components":[{"internalType":"uint16","name":"phaseId","type":"uint16"},{"internalType":"uint80","name":"startingAggregatorRoundId","type":"uint80"},{"internalType":"uint80","name":"endingAggregatorRoundId","type":"uint80"}],"internalType":"struct FeedRegistryInterface.Phase","name":"phase","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"uint16","name":"phaseId","type":"uint16"}],"name":"getPhaseFeed","outputs":[{"internalType":"contract AggregatorV2V3Interface","name":"aggregator","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"uint16","name":"phaseId","type":"uint16"}],"name":"getPhaseRange","outputs":[{"internalType":"uint80","name":"startingRoundId","type":"uint80"},{"internalType":"uint80","name":"endingRoundId","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"uint80","name":"roundId","type":"uint80"}],"name":"getPreviousRoundId","outputs":[{"internalType":"uint80","name":"previousRoundId","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"getProposedFeed","outputs":[{"internalType":"contract AggregatorV2V3Interface","name":"proposedAggregator","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"uint80","name":"roundId","type":"uint80"}],"name":"getRoundFeed","outputs":[{"internalType":"contract AggregatorV2V3Interface","name":"aggregator","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"uint256","name":"roundId","type":"uint256"}],"name":"getTimestamp","outputs":[{"internalType":"uint256","name":"timestamp","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"aggregator","type":"address"}],"name":"isFeedEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"latestAnswer","outputs":[{"internalType":"int256","name":"answer","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"latestRound","outputs":[{"internalType":"uint256","name":"roundId","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"latestTimestamp","outputs":[{"internalType":"uint256","name":"timestamp","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"address","name":"aggregator","type":"address"}],"name":"proposeFeed","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"},{"internalType":"uint80","name":"roundId","type":"uint80"}],"name":"proposedGetRoundData","outputs":[{"internalType":"uint80","name":"id","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"proposedLatestRoundData","outputs":[{"internalType":"uint80","name":"id","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract AccessControllerInterface","name":"_accessController","type":"address"}],"name":"setAccessController","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"typeAndVersion","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
CHAIN_LINK_ABI = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'


AccessControlledOffchainAggregator_ABI='[{"inputs":[{"internalType":"uint32","name":"_maximumGasPrice","type":"uint32"},{"internalType":"uint32","name":"_reasonableGasPrice","type":"uint32"},{"internalType":"uint32","name":"_microLinkPerEth","type":"uint32"},{"internalType":"uint32","name":"_linkGweiPerObservation","type":"uint32"},{"internalType":"uint32","name":"_linkGweiPerTransmission","type":"uint32"},{"internalType":"address","name":"_link","type":"address"},{"internalType":"int192","name":"_minAnswer","type":"int192"},{"internalType":"int192","name":"_maxAnswer","type":"int192"},{"internalType":"contract AccessControllerInterface","name":"_billingAccessController","type":"address"},{"internalType":"contract AccessControllerInterface","name":"_requesterAccessController","type":"address"},{"internalType":"uint8","name":"_decimals","type":"uint8"},{"internalType":"string","name":"description","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"}],"name":"AddedAccess","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"int256","name":"current","type":"int256"},{"indexed":true,"internalType":"uint256","name":"roundId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"updatedAt","type":"uint256"}],"name":"AnswerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"contract AccessControllerInterface","name":"old","type":"address"},{"indexed":false,"internalType":"contract AccessControllerInterface","name":"current","type":"address"}],"name":"BillingAccessControllerSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"maximumGasPrice","type":"uint32"},{"indexed":false,"internalType":"uint32","name":"reasonableGasPrice","type":"uint32"},{"indexed":false,"internalType":"uint32","name":"microLinkPerEth","type":"uint32"},{"indexed":false,"internalType":"uint32","name":"linkGweiPerObservation","type":"uint32"},{"indexed":false,"internalType":"uint32","name":"linkGweiPerTransmission","type":"uint32"}],"name":"BillingSet","type":"event"},{"anonymous":false,"inputs":[],"name":"CheckAccessDisabled","type":"event"},{"anonymous":false,"inputs":[],"name":"CheckAccessEnabled","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"previousConfigBlockNumber","type":"uint32"},{"indexed":false,"internalType":"uint64","name":"configCount","type":"uint64"},{"indexed":false,"internalType":"address[]","name":"signers","type":"address[]"},{"indexed":false,"internalType":"address[]","name":"transmitters","type":"address[]"},{"indexed":false,"internalType":"uint8","name":"threshold","type":"uint8"},{"indexed":false,"internalType":"uint64","name":"encodedConfigVersion","type":"uint64"},{"indexed":false,"internalType":"bytes","name":"encoded","type":"bytes"}],"name":"ConfigSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"roundId","type":"uint256"},{"indexed":true,"internalType":"address","name":"startedBy","type":"address"},{"indexed":false,"internalType":"uint256","name":"startedAt","type":"uint256"}],"name":"NewRound","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint32","name":"aggregatorRoundId","type":"uint32"},{"indexed":false,"internalType":"int192","name":"answer","type":"int192"},{"indexed":false,"internalType":"address","name":"transmitter","type":"address"},{"indexed":false,"internalType":"int192[]","name":"observations","type":"int192[]"},{"indexed":false,"internalType":"bytes","name":"observers","type":"bytes"},{"indexed":false,"internalType":"bytes32","name":"rawReportContext","type":"bytes32"}],"name":"NewTransmission","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"transmitter","type":"address"},{"indexed":false,"internalType":"address","name":"payee","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"OraclePaid","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"transmitter","type":"address"},{"indexed":true,"internalType":"address","name":"current","type":"address"},{"indexed":true,"internalType":"address","name":"proposed","type":"address"}],"name":"PayeeshipTransferRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"transmitter","type":"address"},{"indexed":true,"internalType":"address","name":"previous","type":"address"},{"indexed":true,"internalType":"address","name":"current","type":"address"}],"name":"PayeeshipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"}],"name":"RemovedAccess","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"contract AccessControllerInterface","name":"old","type":"address"},{"indexed":false,"internalType":"contract AccessControllerInterface","name":"current","type":"address"}],"name":"RequesterAccessControllerSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"requester","type":"address"},{"indexed":false,"internalType":"bytes16","name":"configDigest","type":"bytes16"},{"indexed":false,"internalType":"uint32","name":"epoch","type":"uint32"},{"indexed":false,"internalType":"uint8","name":"round","type":"uint8"}],"name":"RoundRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract AggregatorValidatorInterface","name":"previousValidator","type":"address"},{"indexed":false,"internalType":"uint32","name":"previousGasLimit","type":"uint32"},{"indexed":true,"internalType":"contract AggregatorValidatorInterface","name":"currentValidator","type":"address"},{"indexed":false,"internalType":"uint32","name":"currentGasLimit","type":"uint32"}],"name":"ValidatorConfigSet","type":"event"},{"inputs":[],"name":"LINK","outputs":[{"internalType":"contract LinkTokenInterface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_transmitter","type":"address"}],"name":"acceptPayeeship","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"addAccess","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"billingAccessController","outputs":[{"internalType":"contract AccessControllerInterface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"checkEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"disableAccessCheck","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"enableAccessCheck","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_roundId","type":"uint256"}],"name":"getAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBilling","outputs":[{"internalType":"uint32","name":"maximumGasPrice","type":"uint32"},{"internalType":"uint32","name":"reasonableGasPrice","type":"uint32"},{"internalType":"uint32","name":"microLinkPerEth","type":"uint32"},{"internalType":"uint32","name":"linkGweiPerObservation","type":"uint32"},{"internalType":"uint32","name":"linkGweiPerTransmission","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_roundId","type":"uint256"}],"name":"getTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"},{"internalType":"bytes","name":"_calldata","type":"bytes"}],"name":"hasAccess","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestConfigDetails","outputs":[{"internalType":"uint32","name":"configCount","type":"uint32"},{"internalType":"uint32","name":"blockNumber","type":"uint32"},{"internalType":"bytes16","name":"configDigest","type":"bytes16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRound","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestTransmissionDetails","outputs":[{"internalType":"bytes16","name":"configDigest","type":"bytes16"},{"internalType":"uint32","name":"epoch","type":"uint32"},{"internalType":"uint8","name":"round","type":"uint8"},{"internalType":"int192","name":"latestAnswer","type":"int192"},{"internalType":"uint64","name":"latestTimestamp","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"linkAvailableForPayment","outputs":[{"internalType":"int256","name":"availableBalance","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxAnswer","outputs":[{"internalType":"int192","name":"","type":"int192"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minAnswer","outputs":[{"internalType":"int192","name":"","type":"int192"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_signerOrTransmitter","type":"address"}],"name":"oracleObservationCount","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_transmitter","type":"address"}],"name":"owedPayment","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address payable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"removeAccess","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"requestNewRound","outputs":[{"internalType":"uint80","name":"","type":"uint80"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"requesterAccessController","outputs":[{"internalType":"contract AccessControllerInterface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"_maximumGasPrice","type":"uint32"},{"internalType":"uint32","name":"_reasonableGasPrice","type":"uint32"},{"internalType":"uint32","name":"_microLinkPerEth","type":"uint32"},{"internalType":"uint32","name":"_linkGweiPerObservation","type":"uint32"},{"internalType":"uint32","name":"_linkGweiPerTransmission","type":"uint32"}],"name":"setBilling","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract AccessControllerInterface","name":"_billingAccessController","type":"address"}],"name":"setBillingAccessController","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"_signers","type":"address[]"},{"internalType":"address[]","name":"_transmitters","type":"address[]"},{"internalType":"uint8","name":"_threshold","type":"uint8"},{"internalType":"uint64","name":"_encodedConfigVersion","type":"uint64"},{"internalType":"bytes","name":"_encoded","type":"bytes"}],"name":"setConfig","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"_transmitters","type":"address[]"},{"internalType":"address[]","name":"_payees","type":"address[]"}],"name":"setPayees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract AccessControllerInterface","name":"_requesterAccessController","type":"address"}],"name":"setRequesterAccessController","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract AggregatorValidatorInterface","name":"_newValidator","type":"address"},{"internalType":"uint32","name":"_newGasLimit","type":"uint32"}],"name":"setValidatorConfig","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_transmitter","type":"address"},{"internalType":"address","name":"_proposed","type":"address"}],"name":"transferPayeeship","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"_report","type":"bytes"},{"internalType":"bytes32[]","name":"_rs","type":"bytes32[]"},{"internalType":"bytes32[]","name":"_ss","type":"bytes32[]"},{"internalType":"bytes32","name":"_rawVs","type":"bytes32"}],"name":"transmit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"transmitters","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"typeAndVersion","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"validatorConfig","outputs":[{"internalType":"contract AggregatorValidatorInterface","name":"validator","type":"address"},{"internalType":"uint32","name":"gasLimit","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_recipient","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawFunds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_transmitter","type":"address"}],"name":"withdrawPayment","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

'''ETH/USD aggregator address'''
AccessControlledOffchainAggregator_Address ='0x37bC7498f4FF12C19678ee8fE19d713b87F6a9e6'

'''See here: https://github.com/smartcontractkit/chainlink/blob/master/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol
'''

def get_price_from_aggregator(agg_addr):
    web3 = Web3(Web3.HTTPProvider(config.Infura_EndPoint))
    contract = web3.eth.contract(address=agg_addr, abi=AccessControlledOffchainAggregator_ABI)

    decimals = contract.functions.decimals().call()
    ret = contract.functions.latestRoundData().call()
    round_id, price, started_at, timestamp, answered_in_round = ret
    return round_id, price / 10 ** decimals, started_at, timestamp, answered_in_round

def get_decimals_from_aggregator(agg_addr):
    web3 = Web3(Web3.HTTPProvider(config.Infura_EndPoint))
    contract = web3.eth.contract(address=agg_addr, abi=AccessControlledOffchainAggregator_ABI)
    decimals = contract.functions.decimals().call()
    return decimals


def get_aggregator(base, quote):
    abi = CHAIN_LINK_FEED_REG_ABI
    address = CHAIN_LINK_FEED_REG_ADDR
    web3 = Web3(Web3.HTTPProvider(config.Infura_EndPoint))
    contract = web3.eth.contract(address=address, abi=abi)
    aggregator = contract.functions.getFeed(base=base, quote=quote).call()
    return aggregator

def find_pair_aggregator(base, quote):
    try:
        aggregator = get_aggregator(base=base, quote=quote)
        failed = False
        direct = True
    except:
        failed = True

    if failed:
        try:
            aggregator = get_aggregator(base=quote, quote=base)
            failed = False
            direct = False
        except:
            failed = True

    if not failed:
        return direct, aggregator
    else:
        return None, None

def get_feed_address(from_asset,to_asset):

    web3 = Web3(Web3.HTTPProvider(config.Infura_EndPoint))
    ns = ENS.fromWeb3(web3)
    ens = "{}-{}.data.eth".format(from_asset.lower(), to_asset.lower())
    address = ns.address(ens)
    if address is not None:
        return True, address
    else:
        """Try inverse"""
        inv_ens = "{}-{}.data.eth".format(to_asset.lower(), from_asset.lower())
        inv_address = ns.address(inv_ens)
        if inv_address is not None:
            return False, inv_address

    return None, None


def get_contract_addr_from_local_reg(base, quote):
    return CHAIN_LINK_ADDR[base][quote]

def get_decimals(address):
    web3 = Web3(Web3.HTTPProvider(config.Infura_EndPoint))
    contract = web3.eth.contract(address=address, abi=CHAIN_LINK_ABI)
    decimals = contract.functions.decimals().call()
    return decimals

'''See here: https://docs.chain.link/docs/get-the-latest-price/
'''
def get_price(address, decimals):

    web3 = Web3(Web3.HTTPProvider(config.Infura_EndPoint))
    contract = web3.eth.contract(address=address, abi=CHAIN_LINK_ABI)
    ret = contract.functions.latestRoundData().call()
    round_id, price, started_at, timestamp, answered_in_round = ret
    return round_id, price/ 10**decimals, started_at, timestamp, answered_in_round

'''See here: https://docs.chain.link/docs/get-the-latest-price/
'''
def get_price_from_reg(base, quote, decimals=None):
    web3 = Web3(Web3.HTTPProvider(config.Infura_EndPoint))
    contract = web3.eth.contract(address=CHAIN_LINK_FEED_REG_ADDR, abi=CHAIN_LINK_FEED_REG_ABI)
    ret = contract.functions.latestRoundData(base, quote).call()
    round_id, price, started_at, timestamp, answered_in_round = ret
    if price is not None:
        return round_id, price/ 10**decimals, started_at, timestamp, answered_in_round
    else:
        return round_id, price, started_at, timestamp, answered_in_round


def get_decimals_from_reg(base, quote):
    web3 = Web3(Web3.HTTPProvider(config.Infura_EndPoint))
    contract = web3.eth.contract(address=CHAIN_LINK_FEED_REG_ADDR, abi=CHAIN_LINK_FEED_REG_ABI)
    decimals = contract.functions.decimals(base, quote).call()
    return decimals



if __name__ == '__main__':
    ETH = 'EeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    LINK = '0x514910771AF9Ca656af840dff83E8264EcF986CA'
    col_to_eth_decimals = get_price_from_reg(base=ETH, quote=LINK)
    pass
    '''
    import datetime
    asset_pair = 'ETH_USD'
    decimals = get_decimals(asset_pair=asset_pair)
    for _ in range(100):
        t1 = datetime.datetime.now()
        round_id, price, started_at, timestamp, answered_in_round = get_price(asset_pair=asset_pair, decimals=decimals)
        t2 = datetime.datetime.now()
        print('round_id:{},price:{},started_at:{},timestamp:{},answered_in_round:{},time:{}'.
              format(round_id, price, started_at, timestamp, answered_in_round, (t2-t2)))
    pass
    '''


