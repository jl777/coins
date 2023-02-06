#!/usr/bin/env python3
import os
import sys
import time
import json
import requests
from scan_electrums import get_electrums_report

current_time = time.time()
script_path = os.path.abspath(os.path.dirname(__file__))
repo_path = script_path.replace("/utils", "")
os.chdir(script_path)

# TODO: Check all coins have an icon.
icons = [f for f in os.listdir(f"{repo_path}/icons") if os.path.isfile(f"{repo_path}/icons/{f}.png")]
lightwallet_coins = [f for f in os.listdir(f"{repo_path}/light_wallet_d") if os.path.isfile(f"{repo_path}/light_wallet_d/{f}")]
electrum_coins = [f for f in os.listdir(f"{repo_path}/electrums") if os.path.isfile(f"{repo_path}/electrums/{f}")]
ethereum_coins = [f for f in os.listdir(f"{repo_path}/ethereum") if os.path.isfile(f"{repo_path}/ethereum/{f}")]
explorer_coins = [f for f in os.listdir(f"{repo_path}/explorers") if os.path.isfile(f"{repo_path}/explorers/{f}")]

get_electrums_report()
with open("electrum_scan_report.json", "r") as f:
    electrum_scan_report = json.load(f)

with open("../explorers/explorer_paths.json", "r") as f:
    explorer_paths = json.load(f)

with open("../api_ids/forex_ids.json", "r") as f:
    forex_ids = json.load(f)

with open("../api_ids/nomics_ids.json", "r") as f:
    nomics_ids = json.load(f)

with open("../api_ids/coingecko_ids.json", "r") as f:
    coingecko_ids = json.load(f)

with open("../api_ids/coinpaprika_ids.json", "r") as f:
    coinpaprika_ids = json.load(f)

with open("../slp/bchd_urls.json", "r") as f:
    bchd_urls = json.load(f)

def colorize(string, color):
    colors = {
            'red':'\033[31m',
            'yellow':'\033[33m',
            'magenta':'\033[35m',
            'blue':'\033[34m',
            'green':'\033[32m'
    }
    if color not in colors:
            return str(string)
    else:
            return colors[color] + str(string) + '\033[0m'

class CoinConfig:
    def __init__(self, coin_data: dict):

        self.coin_data = coin_data
        self.data = {}
        self.is_testnet = self.is_testnet_network()
        self.ticker = self.coin_data["coin"].replace("-TEST", "")
        self.base_ticker = self.ticker.split("-")[0]
        self.protocols = {
            "AVAX": "AVX-20",
            "BNB": "BEP-20",
            "ETC": "Ethereum Classic",
            "ETH": "ERC-20",
            "ETH-ARB20": "Arbitrum",
            "FTM": "FTM-20",
            "GLMR": "Moonbeam",
            "HT": "HecoChain",
            "KCS": "KRC-20",
            "MATIC": "Matic",
            "MOVR": "Moonriver",
            "ONE": "HRC-20",
            "QTUM": "QRC-20",
            "RBTC": "RSK Smart Bitcoin",
            "SBCH": "SmartBCH",
            "SLP": "SLPTOKEN",
            "ATOM": "TENDERMINT",
            "OSMO": "TENDERMINT",
            "IRIS": "TENDERMINT",
            "UBQ": "Ubiq"
        }
        self.testnet_protocols = {
            "AVAXT": "AVX-20",
            "BNBT": "BEP-20",
            "FTMT": "FTM-20",
            "tSLP": "SLPTOKEN",
            "tQTUM": "QRC-20",
            "tIRIS": "TENDERMINT",
            "MATICTEST": "Matic",
            "UBQ": "Ubiq"
        }
        self.coin_type = coin_data["protocol"]["type"]
        self.data.update({
            self.ticker: {
                "coin": self.ticker,
                "type": "",
                "name": "",
                "coinpaprika_id": "",
                "coingecko_id": "",
                "nomics_id": "",
                "explorer_url": "",
                "explorer_tx_url": "",
                "explorer_address_url": "",
                "supported": [],
                "active": False,
                "is_testnet": self.is_testnet,
                "currently_enabled": False,
                "wallet_only": False
            }
        })
        if self.coin_type in ["UTXO", "QRC20", "BCH", "QTUM"]:
            try:
                if self.coin_data["sign_message_prefix"]:
                    self.data[self.ticker].update({"sign_message_prefix": coin_data["sign_message_prefix"]})
                else:
                    self.data[self.ticker].update({"sign_message_prefix": ""})
            except KeyError as e:
                print(self.ticker + ': Sign message was not found\n')
            if self.ticker in ["BCH", "tBCH"]:
                self.data[self.ticker].update({
                    "type": "UTXO",
                    "bchd_urls": [],
                    "other_types": ["SLP"]
                })
        elif self.coin_type in ["ZHTLC"]:
            if self.ticker in lightwallet_coins:
                with open(f"../light_wallet_d/{self.ticker}", "r") as f:
                    lightwallet_servers = json.load(f)
                self.data[self.ticker].update({
                    "light_wallet_d_servers": lightwallet_servers
                })
            else:
                self.data[self.ticker].update({
                    "light_wallet_d_servers": []
                })

    def get_protocol_info(self):
        if "protocol_data" in self.coin_data["protocol"]:
            protocol_data = self.coin_data["protocol"]["protocol_data"]
            if "consensus_params" in protocol_data:
                # TODO: ZHTLC things
                self.data[self.ticker].update({
                    "type": self.coin_type
                })

            if "slp_prefix" in protocol_data:
                if self.ticker in ["BCH", "tBCH"]:
                    self.data[self.ticker].update({
                        "allow_slp_unsafe_conf": False
                    })
                    coin_type = "UTXO"
                else:
                    coin_type = "SLP"
                self.data[self.ticker].update({
                    "type": coin_type,
                    "slp_prefix": protocol_data["slp_prefix"]
                })
                if "token_id" in protocol_data:
                    self.data[self.ticker].update({
                        "token_id": protocol_data["token_id"]
                    })

            elif "platform" in protocol_data:
                # TODO: ERC-like things
                platform = protocol_data["platform"]
                if self.is_testnet:
                    coin_type = self.testnet_protocols[platform]
                else:
                    coin_type = self.protocols[platform]
                self.data[self.ticker].update({"type": coin_type})
                if "contract_address" in protocol_data: 
                    self.data[self.ticker].update({
                        "contract_address": protocol_data["contract_address"]
                    })
        else:
            self.data[self.ticker].update({
                "type": self.coin_type
            })

        self.parent_coin = self.get_parent_coin()
        if self.parent_coin:
            if self.parent_coin != self.ticker:
                self.data[self.ticker].update({
                    "parent_coin": self.parent_coin
                })

        if self.coin_data["protocol"]["type"] in ["ETH", "QTUM"]:
            if self.ticker in self.protocols:
                coin_type = self.protocols[self.ticker]
            elif self.ticker in self.testnet_protocols:
                coin_type = self.testnet_protocols[self.ticker]
            elif self.parent_coin in self.protocols:
                coin_type = self.protocols[self.parent_coin]
            elif self.parent_coin in self.testnet_protocols:
                coin_type = self.testnet_protocols[self.parent_coin]
            else:
                coin_type = self.coin_data["protocol"]["type"]
            self.data[self.ticker].update({"type": coin_type})

        elif self.coin_data["protocol"]["type"] in ["TENDERMINT", "TENDERMINTTOKEN"]:
            coin_type = self.coin_data["protocol"]["type"]
            self.data[self.ticker].update({"type": coin_type})

    def is_testnet_network(self):
        if "is_testnet" in self.coin_data:
            return self.coin_data["is_testnet"]
        return False

    def get_forex_id(self):
        coin = self.ticker.replace('-segwit', '')
        if coin in forex_ids:
            self.data[self.ticker].update({
                "forex_id": forex_ids[coin]
            })

    def get_coinpaprika_id(self):
        coin = self.ticker.replace('-segwit', '')
        if coin in coinpaprika_ids:
            self.data[self.ticker].update({
                "coinpaprika_id": coinpaprika_ids[coin]
            })

    def get_coingecko_id(self):
        coin = self.ticker.replace('-segwit', '')
        if coin in coingecko_ids:
            self.data[self.ticker].update({
                "coingecko_id": coingecko_ids[coin]
            })

    def get_nomics_id(self):
        coin = self.ticker.replace('-segwit', '')
        if coin in nomics_ids:
            self.data[self.ticker].update({
                "nomics_id": nomics_ids[coin]
            })

    def get_alias_ticker(self):
        if "alias_ticker" in self.coin_data:
            self.data[self.ticker].update({
                "alias_ticker": self.coin_data["alias_ticker"]
            })

    def get_asset(self):
        if "asset" in self.coin_data:
            self.data[self.ticker].update({
                "asset": self.coin_data["asset"]
            })

    def get_links(self):
        if "links" in self.coin_data:
            self.data[self.ticker].update({
                "links": self.coin_data["links"]
            })

    def get_hd_info(self):
        if "derivation_path" in self.coin_data:
            self.data[self.ticker].update({
                "derivation_path": self.coin_data["derivation_path"]
            })
        if "trezor_coin" in self.coin_data:
            self.data[self.ticker].update({
                "trezor_coin": self.coin_data["trezor_coin"]
            })


    def get_rewards_info(self):
        if self.ticker in ["KMD"]:
            self.data[self.ticker].update({
                "is_claimable": True,
                "minimal_claim_amount": "10"
            })

    def get_address_format(self):
        if "address_format" in self.coin_data:
            self.data[self.ticker].update({"address_format": self.coin_data["address_format"]})

        if self.ticker.find('-segwit') > -1:
            self.data[self.ticker].update({"address_format": {"format":"segwit"}})

    def is_smartchain(self):
        if "sign_message_prefix" in self.coin_data:
            if self.coin_data["sign_message_prefix"] == "Komodo Signed Message:\n":
                self.data[self.ticker]["type"] = "Smart Chain"

    def is_wallet_only(self):
        if "wallet_only" in self.coin_data:
            self.data[self.ticker].update({
                "wallet_only": self.coin_data["wallet_only"]
            })

    def get_parent_coin(self):
        ''' Used for getting filename for related coins/ethereum folder '''
        token_type = self.data[self.ticker]["type"]
        if self.ticker == "RBTC":
            return "RSK"
        if token_type in ["SLP"]:
            if self.data[self.ticker]["is_testnet"]:
                return f"t{token_type}"
            return token_type

        if self.coin_type in ["TENDERMINTTOKEN", "TENDERMINT"]:
            if self.ticker.find("_ATOM") > -1:
                return "ATOM"
            elif self.ticker.find("_IRIS") > -1:
                if self.data[self.ticker]["is_testnet"]:
                    return "tIRIS"
                return "IRIS"
            elif self.ticker.find("_OSMO") > -1:
                return "OSMO"

        if self.coin_type not in ["UTXO", "ZHTLC", "BCH", "QTUM"]:
            if self.data[self.ticker]["is_testnet"]:
                key_list = list(self.testnet_protocols.keys())
                value_list = list(self.testnet_protocols.values())
            else:
                key_list = list(self.protocols.keys())
                value_list = list(self.protocols.values())
            if self.ticker in key_list:
                return self.ticker
            
            if self.ticker == "RBTC": token_type = "RSK Smart Bitcoin"
            if token_type in value_list:
                i = value_list.index(token_type)
                return key_list[i]
            print(f"{token_type} not in value_list")
        return None

    def clean_name(self):
        self.data[self.ticker].update({"name":self.coin_data["fname"]})

    def get_electrums(self):
        coin = self.ticker.replace('-segwit', '')
        if self.data[self.ticker]["type"] == "QRC-20":
            if self.is_testnet:
                coin = "tQTUM"
            else:
                coin = "QTUM"

        if coin in electrum_scan_report:
            with open(f"../electrums/{coin}", "r") as f:
                electrums = json.load(f)
                valid_electrums = []
                for x in ["tcp", "ssl"]:
                    # This also filers ws with tcp/ssl server it is grouped with if valid.
                    for k, v in electrum_scan_report[coin][x].items():
                        if current_time - v["last_connection"] < 604800: # 1 week grace period
                            for electrum in electrums:
                                if electrum["url"] == k:
                                    valid_electrums.append(electrum)

                self.data[self.ticker].update({
                    "electrum": valid_electrums
                })

    def get_bchd_urls(self):
        if self.ticker in bchd_urls:
            self.data[self.ticker].update({
                "bchd_urls": bchd_urls[self.ticker]
            })

    def get_swap_contracts(self):
        # TODO: update swap contracts to post-IRIS once Artem greenlights.
        contract_data = None

        if self.ticker in ethereum_coins:
            with open(f"../ethereum/{self.ticker}", "r") as f:
                contract_data = json.load(f)

        elif self.ticker not in electrum_coins:
            if self.parent_coin not in ["SLP", "tSLP", None]:
                with open(f"../ethereum/{self.parent_coin}", "r") as f:
                    contract_data = json.load(f)

        if contract_data:
            if "swap_contract_address" in contract_data:
                self.data[self.ticker].update({
                    "swap_contract_address": contract_data["swap_contract_address"]
                })
            if "fallback_swap_contract" in contract_data:
                self.data[self.ticker].update({
                    "fallback_swap_contract": contract_data["fallback_swap_contract"]
                })
            if "rpc_nodes" in contract_data:
                if self.data[self.ticker]["type"] in ["TENDERMINT", "TENDERMINTTOKEN"]: key = "rpc_urls"
                else: key = "nodes"
                self.data[self.ticker].update({key: contract_data["rpc_nodes"]})

    def get_explorers(self):
        explorers = None
        coin = self.ticker.replace('-segwit', '')
        if coin in explorer_coins:
            with open(f"../explorers/{coin}", "r") as f:
                explorers = json.load(f)

        elif self.parent_coin in explorer_coins:
            with open(f"../explorers/{self.parent_coin}", "r") as f:
                explorers = json.load(f)

        if explorers:
            for x in explorers:
                for p in explorer_paths:
                    if x.find(p) > -1:
                        self.data[self.ticker].update(explorer_paths[p])
            self.data[self.ticker].update({"explorer_url": explorers[0]})

def parse_coins_repo():
    errors = []
    coins_config = {}
    with open("../coins", "r") as f:
        coins_data = json.load(f)

    for item in coins_data:
        
        if item["mm2"] == 1:
                config = CoinConfig(item)
                config.get_protocol_info()
                config.clean_name()
                config.get_swap_contracts()
                config.get_electrums()
                config.get_explorers()
                config.is_smartchain()
                config.is_wallet_only()
                config.get_address_format()
                config.get_rewards_info()
                config.get_alias_ticker()
                config.get_asset()
                config.get_forex_id()
                config.get_coinpaprika_id()
                config.get_coingecko_id()
                config.get_nomics_id()
                config.get_bchd_urls()
                config.get_hd_info()
                config.get_links()
                coins_config.update(config.data)

    nodata = []
    for coin in coins_config:
        if not coins_config[coin]["explorer_url"]:
            print(f"{coin} has no explorers!")
        if coins_config[coin]["type"] not in ["SLP"]:
            for field in ["nodes", "electrum", "light_wallet_d_servers", "rpc_urls"]:
                if field in coins_config[coin]:
                    if not coins_config[coin][field]:
                        nodata.append(coin)
            if "nodes" not in coins_config[coin] and "electrum" not in coins_config[coin] and "rpc_urls" not in coins_config[coin]:
                nodata.append(coin)

    print(f"The following coins are missing required data or failing connections for nodes/electrums {nodata}")
    print(f"They will not be included in the output")
    if errors:
        print(f"Errors:")
        for error in errors:
            print(error)
    for coin in nodata:
        del coins_config[coin]
    return coins_config


def get_desktop_repo_coins_data():
    ''' for this to work, you need atomicdex-desktop cloned into
        the same folder as you cloned the coins repo. '''
    desktop_coins_folder = "../../atomicDEX-Desktop/assets/config/"
    contents = os.listdir(desktop_coins_folder)
    for f in contents:
        if f.endswith("coins.json"):
            coins_fn = f
    with open(f"../../atomicDEX-Desktop/assets/config/{coins_fn}", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    coins_config = parse_coins_repo()
    with open("coins_config.json", "w+") as f:
        json.dump(coins_config, f, indent=4)
