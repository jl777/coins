#!/usr/bin/env python3
import os
import json
from pprint import pprint
import requests

electrum_coins = os.listdir("../electrums")
ethereum_coins = os.listdir("../ethereum")
explorer_coins = os.listdir("../explorers")

with open("../explorers/explorer_paths.json", "r") as f:
    explorer_paths = json.load(f)

class CoinConfig:
    def __init__(self, coin_data: dict):

        self.coin_data = coin_data
        self.data = {}
        self.ticker = self.coin_data["coin"]
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
            "UBQ": "Ubiq"
        }
        self.testnet_protocols = {
            "AVAXT": "AVX-20",
            "BNBT": "BEP-20",
            "FTMT": "FTM-20",
            "tSLP": "SLPTOKEN",
            "tQTUM": "QRC-20",
            "MATICTEST": "Matic Testnet",
            "UBQ": "Ubiq"
        }

        self.coin_type = coin_data["protocol"]["type"]
        if self.coin_type in ["SLPTOKEN"]:
            self.data.update({
                self.ticker: {
                    "coin": self.ticker,
                    "type": "SLP",
                    "name": "",
                    "coinpaprika_id": "",
                    "coingecko_id": "",
                    "nomics_id": "",
                    "explorer_url": [],
                    "explorer_tx_url": "",
                    "explorer_address_url": "",
                    "supported": [],
                    "active": False,
                    "is_testnet": self.is_testnet_network(),
                    "currently_enabled": False
                }
            })
        elif self.coin_type in ["UTXO", "QRC20", "BCH", "QTUM"]:
            self.data.update({
                self.ticker: {
                    "coin": self.ticker,
                    "type": "",
                    "name": "",
                    "sign_message_prefix": "",
                    "coinpaprika_id": "",
                    "coingecko_id": "",
                    "nomics_id": "",
                    "electrum": [],
                    "explorer_url": [],
                    "explorer_tx_url": "",
                    "explorer_address_url": "",
                    "supported": [],
                    "active": False,
                    "is_testnet": self.is_testnet_network(),
                    "currently_enabled": False
                }
            })
            if self.ticker in ["BCH", "tBCH"]:
                self.data[self.ticker].update({
                    "type": "UTXO",
                    "bchd_urls": [],
                    "other_types": ["SLP"]
                })                

        elif self.coin_type in ["ETH", "ERC20"]:
            self.data.update({
                self.ticker: {
                    "coin": self.ticker,
                    "type": "",
                    "name": "",
                    "coinpaprika_id": "",
                    "coingecko_id": "",
                    "nomics_id": "",
                    "nodes": [],
                    "explorer_url": [],
                    "explorer_tx_url": "",
                    "explorer_address_url": "",
                    "supported": [],
                    "active": False,
                    "is_testnet": self.is_testnet_network(),
                    "currently_enabled": False,
                    "contract_address": "",
                    "swap_contract_address": "",
                    "fallback_swap_contract": "",
                }
            })
        elif self.coin_type in ["ZHTLC"]:
            self.data.update({
                self.ticker: {
                    "coin": self.ticker,
                    "type": "",
                    "name": "",
                    "coinpaprika_id": "",
                    "coingecko_id": "",
                    "nomics_id": "",
                    "electrum": [],
                    "explorer_url": [],
                    "light_wallet_d_servers": [],
                    "explorer_tx_url": "",
                    "explorer_address_url": "",
                    "supported": [],
                    "active": False,
                    "is_testnet": self.is_testnet_network(),
                    "currently_enabled": False,
                    "contract_address": ""
                }
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
                if self.is_testnet_network():
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

    def is_testnet_network(self):
        if "is_testnet" in self.coin_data:
            return self.coin_data["is_testnet"]
        return False

    def get_parent_coin(self):
        ''' Used for getting filename for related coins/ethereum folder '''
        if self.coin_type not in ["UTXO", "ZHTLC", "BCH", "QTUM"]:
            if self.data[self.ticker]["is_testnet"]:
                key_list = list(self.testnet_protocols.keys())
                value_list = list(self.testnet_protocols.values())
            else:
                key_list = list(self.protocols.keys())
                value_list = list(self.protocols.values())
            if self.ticker in key_list:
                return self.ticker
            token_type = self.data[self.ticker]["type"]
            if token_type  == "SLP": return "BCH"
            if token_type  == "tSLP": return "tBCH"
            #if token_type == "ETH": print(self.data)
            if self.ticker == "RBTC": token_type = "RSK Smart Bitcoin"
            i = value_list.index(token_type)
            return key_list[i]
        return None

    def clean_name(self):
        name = self.coin_data["fname"].lower()
        if name == self.base_ticker.lower(): self.name = name.upper()
        if name.find('token'): name.replace('token', ' token')
        self.data[self.ticker].update({"name":name.title()})

    def get_electrums(self):
        with open(f"../electrums/{self.ticker}", "r") as f:
            self.data[self.ticker].update({
                "electrum": json.load(f)
            })

    def get_swap_contracts(self):
        # TODO: update swap contracts to post-IRIS once Artem greenlights.
        contract_data = None
        if self.ticker in ethereum_coins:
            with open(f"../ethereum/{self.ticker}", "r") as f:
                contract_data = json.load(f)
        elif self.ticker not in electrum_coins:
            parent_coin = self.get_parent_coin()
            if self.ticker == "RBTC":
                parent_coin = "RSK"
                with open(f"../ethereum/{parent_coin}", "r") as f:
                    contract_data = json.load(f)
            elif parent_coin not in ["QTUM", "tQTUM", "BCH", "tBCH", None]:
                with open(f"../ethereum/{parent_coin}", "r") as f:
                    contract_data = json.load(f)

        if contract_data:
            nodes = [i["url"] for i in contract_data["rpc_nodes"]]
            self.data[self.ticker].update({
                "nodes": nodes,
                "swap_contract_address": contract_data["swap_contract_address"]
            })
            if "fallback_swap_contract" in contract_data:
                self.data[self.ticker].update({
                    "fallback_swap_contract": contract_data["fallback_swap_contract"]
                })


    def get_explorers(self):
        explorers = []
        ticker = self.ticker.replace("-segwit", "").replace("-TEST", "")
        parent_coin = self.get_parent_coin()
        if ticker in explorer_coins:
            with open(f"../explorers/{ticker}", "r") as f:
                explorers = json.load(f)
                for x in explorers:
                    for i in ["tx/"]:
                        if x.endswith(i):
                            x = x[:-1*(len(i))]
                            self.data[self.ticker].update({"explorer_tx_url": i})

                    for p in explorer_paths:
                        if x.find(p) > -1:
                            self.data[self.ticker].update(explorer_paths[p])

        elif parent_coin in explorer_coins:
            with open(f"../explorers/{parent_coin}", "r") as f:
                explorers = json.load(f)

        if explorers:
            self.data[self.ticker].update({"explorer_url": explorers})

def parse_coins_repo():

    desktop_coins = {}
    with open("../coins", "r") as f:
        coins_data = json.load(f)

    for item in coins_data:
        if item["mm2"] == 1:
            config = CoinConfig(item)
            config.get_protocol_info()
            config.clean_name()
            config.get_swap_contracts()

            if item["coin"] in electrum_coins:
                config.get_electrums()

            config.get_explorers()


            desktop_coins.update(config.data)

    for coin in desktop_coins:
        if not desktop_coins[coin]["explorer_url"]:
            print(f"{coin} has no explorers!")

    with open("desktop_coins.json", "w+") as f:
        json.dump(desktop_coins, f, indent=4)


if __name__ == "__main__":
    parse_coins_repo()
