#!/usr/bin/env python3
import os
import json
from pprint import pprint
import requests

electrum_coins = os.listdir("../electrums")
explorer_coins = os.listdir("../explorers")
ethereum_coins = os.listdir("../ethereum")


class CoinConfig:
    def __init__(self, coin_data: dict):

        self.coin_data = coin_data
        self.data = {}
        self.ticker = self.coin_data["coin"]
        self.base_ticker = self.ticker.split("-")[0]
        self.protocols = {
            "AVAX": "AVX-20",
            "AVAXT": "AVX-20",
            "BCH": "SLP",
            "BNB": "BEP-20",
            "BNBT": "BEP-20",
            "ETC": "Ethereum Classic",
            "ETH": "ERC-20",
            "ETH-ARB20": "Arbitrum",
            "FTM": "FTM-20",
            "FTMT": "FTM-20",
            "GLMR": "Moonbeam",
            "HT": "HecoChain",
            "KCS": "KRC-20",
            "MATIC": "Matic",
            "MATICTEST": "Matic Testnet",
            "MOVR": "Moonriver",
            "ONE": "HRC-20",
            "QTUM": "QRC-20",
            "RBTC": "RSK Smart Bitcoin",
            "SBCH": "SmartBCH",
            "tQTUM": "QRC-20",
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
                    "is_testnet": False,
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
                    "is_testnet": False,
                    "currently_enabled": False
                }
            })
            if self.ticker in ["BCH", "tBCH"]:
                self.data[self.ticker].update({
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
                    "is_testnet": False,
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
                    "is_testnet": False,
                    "currently_enabled": False,
                    "contract_address": ""
                }
            })

    def get_protocol_info(self):
        
        if self.ticker in self.protocols.keys():
            protocol = self.protocols[self.ticker]
            self.data[self.ticker].update({
                "type": protocol
            })
        elif "protocol_data" in self.coin_data["protocol"]:
            protocol_data = self.coin_data["protocol"]["protocol_data"]
            if "consensus_params" in protocol_data:
                self.data[self.ticker].update({
                    "type": self.coin_type
                })
            elif "token_id" in protocol_data:
                self.data[self.ticker].update({
                    "type": self.coin_type,
                    "token_id": protocol_data["token_id"]
                })
            elif "platform" in protocol_data:
                platform = protocol_data["platform"]
                protocol = self.protocols[platform]
                self.data[self.ticker].update({
                    "type": protocol,
                    "contract_address": protocol_data["contract_address"]
                })
            else:
                self.data[self.ticker].update({
                    "type": "SLP",
                    "slp_prefix": protocol_data["slp_prefix"]
                })

        else:
            self.data[self.ticker].update({
                "type": self.coin_type
            })

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
        contract_data = None
        if self.ticker in ethereum_coins:
            with open(f"../ethereum/{self.ticker}", "r") as f:
                contract_data = json.load(f)
        else:
            parent_coin = self.get_parent_coin()
            if self.ticker == "RBTC":
                parent_coin = "RSK"
            if parent_coin:
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

    def get_parent_coin(self):
        ''' Used for getting filename for related coins/ethereum folder '''
        if self.coin_type not in ["UTXO", "ZHTLC", "BCH", "SLPTOKEN", "QTUM", "QRC20"]:
            key_list = list(self.protocols.keys())
            value_list = list(self.protocols.values())
            token_type = self.data[self.ticker]["type"]
            if self.ticker == "RBTC": token_type = "RSK Smart Bitcoin"
            #if token_type == "ETH": print(self.data)
            i = value_list.index(token_type)
            return key_list[i]
        return None

    def get_explorers(self):
        explorers = []
        if self.data[self.ticker]["type"] == "BEP-20":
            if self.data[self.ticker]["is_testnet"]:
                explorers = ["https://data-seed-prebsc-1-s2.binance.org:8545"]
            else:
                explorers = ["https://bscscan.com/"]

        if self.data[self.ticker]["type"] == "ERC-20":
            explorers = ["https://etherscan.io/"]

        if self.data[self.ticker]["type"] == "AVX-20":
            if self.data[self.ticker]["is_testnet"]:
                explorers = ["https://cchain.explorer.avax-test.network/"]
            else:
                explorers = ["https://snowtrace.io/"]
            
        if self.data[self.ticker]["type"] == "HRC-20":
            explorers = ["https://explorer.harmony.one/"]

        if self.data[self.ticker]["type"] == "KRC-20":
            explorers = ["https://explorer.kcc.io/en/"]

        if self.data[self.ticker]["type"] == "Matic":
            if self.data[self.ticker]["is_testnet"]:
                explorers = ["https://mumbai.polygonscan.com/"]
            else:
                explorers = ["https://polygonscan.com/"]

        if self.data[self.ticker]["type"] == "FTM-20":
            if self.data[self.ticker]["is_testnet"]:
                explorers = ["https://testnet.ftmscan.com/"]
            else:
                explorers = ["https://ftmscan.com/"]

        if self.data[self.ticker]["type"] == "QRC-20":
            if self.data[self.ticker]["is_testnet"]:
                explorers = ["https://testnet.qtum.org/"]
            else:
                explorers = ["https://explorer.qtum.org/"]

        if self.data[self.ticker]["type"] == "Moonriver":
                explorers = ["https://moonriver.moonscan.io/"]

        if self.data[self.ticker]["type"] == "Moonbeam":
                explorers = ["https://rpc.api.moonbeam.network"]

        if self.data[self.ticker]["type"] == "HecoChain":
            explorers = ["https://hecoinfo.com/"]

        if self.data[self.ticker]["type"] == "SLPTOKEN":
            if self.data[self.ticker]["is_testnet"]:
                explorers = ["https://testnet.simpleledger.info/"]
            else:
                explorers = ["https://simpleledger.info/"]

        if self.ticker in explorer_coins:
            with open(f"../explorers/{self.ticker}", "r") as f:
                explorers = json.load(f)
                for x in explorers:
                    for i in ["tx/"]:
                        if x.endswith(i):
                            x = x[:-1*(len(i))]
                            self.data[self.ticker].update({"explorer_tx_url": i})

                    if x.startswith("https://chainz.cryptoid.info/"):
                        self.data[self.ticker].update({
                            "explorer_tx_url": "tx.dws?",
                            "explorer_address_url": "address.dws?"
                        })
                    if x.startswith("https://blockchair.com/"):
                        self.data[self.ticker].update({
                            "explorer_tx_url": "transaction/"
                        })

                    if x in ["https://explorer.zcha.in/"]:
                        self.data[self.ticker].update({
                            "explorer_tx_url": "transactions/"
                        })

                    if x in ["https://explorer.runebase.io/", "https://softbalanced.com:3001/insight/"
                             "https://explorer.fujicoin.org/", "https://explorer.blackcoin.nl/",
                             "https://explorer.lightningcash-coin.com/"
                             ]:
                        self.data[self.ticker].update({
                            "explorer_tx_url": "tx/",
                            "explorer_address_url": "address/"
                        })

                    if x in ["https://testnet.simpleledger.info/", "https://simpleledger.info/"]:
                        self.data[self.ticker].update({
                            "explorer_tx_url": "#tx/"
                        })

                    if x == "https://www.nyanchain.com/":
                        self.data[self.ticker].update({
                            "explorer_tx_url": "tx.nyan?",
                            "explorer_address_url": "ad.nyan?"
                        })
        if explorers:
            self.data[self.ticker].update({"explorer_url": explorers})
        else:
            print(f"no explorers for {self.ticker}")

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


    with open("desktop_coins.json", "w+") as f:
        json.dump(desktop_coins, f, indent=4)


if __name__ == "__main__":
    parse_coins_repo()
