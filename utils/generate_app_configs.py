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
        self.name = name.title()

    def get_electrums(self):
        with open(f"../electrums/{self.ticker}", "r") as f:
            self.data[self.ticker].update({
                "electrum": json.load(f)
            })

    def get_swap_contracts(self):
        contract_data = None
        print(self.ticker)
        print(self.coin_type)
        print(ethereum_coins)
        if self.ticker in ethereum_coins:
            with open(f"../ethereum/{self.ticker}", "r") as f:
                contract_data = json.load(f)
        elif self.coin_type not in ["UTXO", "ZHTLC", "BCH", "SLPTOKEN", "QTUM"]:
            key_list = list(self.protocols.keys())
            value_list = list(self.protocols.values())
            
            token_type = self.coin_type
            if self.ticker == "RBTC": token_type = "RSK Smart Bitcoin"
            if token_type == "ETH": pass
            if token_type.endswith("20"): token_type = token_type.replace("20", "-20")
            i = value_list.index(token_type)
            parent_coin = key_list[i]
            if parent_coin in ethereum_coins:
                with open(f"../ethereum/{key_list[i]}", "r") as f:
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
        if self.coin_type == "BEP20":
            self.data[self.ticker].update({"explorer_url": ["https://bscscan.com/"]})
        if self.coin_type == "ERC20":
            self.data[self.ticker].update({"explorer_url": ["https://etherscan.io/"]})
        if self.coin_type == "AVX20":
            self.data[self.ticker].update({"explorer_url": ["https://snowtrace.io/"]})
        if self.coin_type == "HRC20":
            self.data[self.ticker].update({"explorer_url": ["https://explorer.harmony.one/"]})
        if self.coin_type == "KRC20":
            self.data[self.ticker].update({"explorer_url": ["https://explorer.kcc.io/en/"]})

        elif self.ticker in explorer_coins:
            with open(f"../explorers/{self.ticker}", "r") as f:
                explorers = json.load(f)
                for x in explorers:
                    print(x)
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

                self.data[self.ticker].update({
                    "explorer_url": explorers
                })

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


            print(item["coin"])
            print(item)
            pprint(config.data)
            desktop_coins.update(config.data)

    with open("desktop_coins.json", "w+") as f:
        json.dump(desktop_coins, f, indent=4)


if __name__ == "__main__":
    parse_coins_repo()
