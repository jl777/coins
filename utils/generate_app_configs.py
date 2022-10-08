#!/usr/bin/env python3
import os
import sys
import json
import requests
from scan_electrums import get_electrums_report

os.chdir(os.path.abspath(os.path.dirname(__file__)))

# TODO: Check all coins have an icon.
icons = os.listdir("../icons")
electrum_coins = os.listdir("../electrums")
ethereum_coins = os.listdir("../ethereum")
explorer_coins = os.listdir("../explorers")

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
                "explorer_url": [],
                "explorer_tx_url": "",
                "explorer_address_url": "",
                "supported": [],
                "active": False,
                "is_testnet": self.is_testnet_network(),
                "currently_enabled": False,
                "wallet_only": False
            }
        })
        if self.coin_type in ["UTXO", "QRC20", "BCH", "QTUM"]:
            self.data[self.ticker].update({"sign_message_prefix": ""})
            if self.ticker in ["BCH", "tBCH"]:
                self.data[self.ticker].update({
                    "type": "UTXO",
                    "bchd_urls": [],
                    "other_types": ["SLP"]
                })
        elif self.coin_type in ["ZHTLC"]:
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

        if self.coin_data["protocol"]["type"] in ["ETH", "QTUM"]:
            if self.ticker in self.protocols:
                coin_type = self.protocols[self.ticker]
            elif self.ticker in self.testnet_protocols:
                coin_type = self.testnet_protocols[self.ticker]
            self.data[self.ticker].update({
                "type": coin_type
            })

    def is_testnet_network(self):
        if "is_testnet" in self.coin_data:
            return self.coin_data["is_testnet"]
        return False

    def get_forex_id(self):
        if self.ticker in forex_ids:
            self.data[self.ticker].update({
                "forex_id": forex_ids[self.ticker]
            })

    def get_coinpaprika_id(self):
        if self.ticker in coinpaprika_ids:
            self.data[self.ticker].update({
                "coinpaprika_id": coinpaprika_ids[self.ticker]
            })

    def get_coingecko_id(self):
        if self.ticker in coingecko_ids:
            self.data[self.ticker].update({
                "coingecko_id": coingecko_ids[self.ticker]
            })

    def get_nomics_id(self):
        if self.ticker in nomics_ids:
            self.data[self.ticker].update({
                "nomics_id": nomics_ids[self.ticker]
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

    def get_rewards_info(self):
        if self.ticker in ["KMD"]:
            self.data[self.ticker].update({
                "is_claimable": True,
                "minimal_claim_amount": "10"
            })

    def get_address_format(self):
        if "segwit" in self.coin_data:
            if self.coin_data["segwit"]:
                self.data[self.ticker].update({
                    "is_segwit_on": False,
                    "address_format": {"format":"standard"}
                })
        elif "address_format" in self.coin_data:
            self.data[self.ticker]["address_format"].update(self.coin_data["address_format"])

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
        if token_type in ["SLP"]:
            if self.data[self.ticker]["is_testnet"]:
                return f"t{token_type}"
            return token_type

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
            i = value_list.index(token_type)
            return key_list[i]
        return None

    def clean_name(self):
        self.data[self.ticker].update({"name":self.coin_data["fname"]})

    def get_electrums(self, coin):
        with open(f"../electrums/{coin}", "r") as f:
            electrums = json.load(f)
            valid_electrums = []
            print("-----------------")
            if coin in electrum_scan_report["passed"]:
                for electrum in electrums:
                    if electrum["url"] in electrum_scan_report["passed"][coin]:
                        valid_electrums.append(electrum)

            if coin in electrum_scan_report["passed_ssl"]:
                for electrum in electrums:
                    if electrum["url"] in electrum_scan_report["passed_ssl"][coin]:
                        valid_electrums.append(electrum)
                    
            print(self.ticker)
            print(valid_electrums)
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
            parent_coin = self.get_parent_coin()
            if self.ticker == "RBTC":
                parent_coin = "RSK"
                with open(f"../ethereum/{parent_coin}", "r") as f:
                    contract_data = json.load(f)
            elif parent_coin not in ["QTUM", "tQTUM", "SLP", "tSLP", None]:
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

    def get_explorers(self, ticker):
        explorers = []
        parent_coin = self.get_parent_coin()
        if ticker in explorer_coins:
            with open(f"../explorers/{ticker}", "r") as f:
                explorers = json.load(f)
                for x in explorers:
                    for p in explorer_paths:
                        if x.find(p) > -1:
                            self.data[self.ticker].update(explorer_paths[p])

        elif parent_coin in explorer_coins:
            with open(f"../explorers/{parent_coin}", "r") as f:
                explorers = json.load(f)

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

        if item["mm2"] == 1 and item["coin"].find("-segwit") == -1:
            coin = item["coin"].replace("-TEST", "")
            config = CoinConfig(item)
            config.get_protocol_info()
            config.clean_name()
            config.get_swap_contracts()
            if coin in electrum_coins:
                config.get_electrums(coin)
            config.get_explorers(coin)
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

            desktop_coins.update(config.data)

    for coin in desktop_coins:
        if not desktop_coins[coin]["explorer_url"]:
            print(f"{coin} has no explorers!")
        if ("nodes" not in desktop_coins[coin]
                    and "electrum" not in desktop_coins[coin]
                    and desktop_coins[coin]["type"] not in ["SLP", "QRC-20"]):
            print(f"{coin} has no nodes or electrums!")
            # print(desktop_coins[coin])
    return desktop_coins


def get_desktop_repo_coins_data():
    ''' for this to work, you need atomicdex-desktop cloned into
        the same folder as you cloned the coins repo '''
    desktop_coins_folder = "../../atomicDEX-Desktop/assets/config/"
    contents = os.listdir(desktop_coins_folder)
    for f in contents:
        if f.endswith("coins.json"):
            coins_fn = f
    with open(f"../../atomicDEX-Desktop/assets/config/{coins_fn}", "r") as f:
        return json.load(f)

def get_api_ids_from_desktop():
    desktop_repo_coins = get_desktop_repo_coins_data()
    nomics_ids = {}
    coinpaprika_ids = {}
    coingecko_ids = {}
    forex_ids = {}
    for coin in desktop_repo_coins:
        if "nomics_id" in desktop_repo_coins[coin]:
            if desktop_repo_coins[coin]["nomics_id"]:
                nomics_ids.update({coin: desktop_repo_coins[coin]["nomics_id"]})
        if "coingecko_id" in desktop_repo_coins[coin]:
            if desktop_repo_coins[coin]["coingecko_id"]:
                coingecko_ids.update({coin: desktop_repo_coins[coin]["coingecko_id"]})
        if "coinpaprika_id" in desktop_repo_coins[coin]:
            if desktop_repo_coins[coin]["coinpaprika_id"]:
                coinpaprika_ids.update({coin: desktop_repo_coins[coin]["coinpaprika_id"]})
        if "forex_id" in desktop_repo_coins[coin]:
            if desktop_repo_coins[coin]["forex_id"]:
                forex_ids.update({coin: desktop_repo_coins[coin]["forex_id"]})

    with open("../api_ids/coingecko_ids.json", "w+") as f:
        json.dump(coingecko_ids, f, indent=4)
    with open("../api_ids/coinpaprika_ids.json", "w+") as f:
        json.dump(coinpaprika_ids, f, indent=4)
    with open("../api_ids/nomics_ids.json", "w+") as f:
        json.dump(nomics_ids, f, indent=4)
    with open("../api_ids/forex_ids.json", "w+") as f:
        json.dump(forex_ids, f, indent=4)


def compare_output_vs_desktop_repo(desktop_coins):
    desktop_repo_coins = get_desktop_repo_coins_data()
    errors = {
        "no_value": 0,
        "missing_entry": 0,
        "explorer_mismatch":0,
        "name_mismatch":0,
        "electrum_mismatch":0,
        "ws_mismatch":0,
        "value_mismatch": 0
    }
    for coin in desktop_repo_coins:
        for k, v in desktop_repo_coins[coin].items():
            if k not in desktop_coins[coin]:
                errors["missing_entry"] += 1
                print(colorize(f"{coin} is missing an entry for {k} in script output", 'blue'))
            else:
                if desktop_coins[coin][k]:
                    try:
                        if isinstance(desktop_coins[coin][k], list):
                            # TODO: loop for electum comparison
                            if not isinstance(v[0], dict):
                                assert set(desktop_coins[coin][k]) == set(v)
                            else:
                                script_electrums = set([x["url"] for x in v])
                                desktop_repo_electrums = set([x["url"] for x in desktop_coins[coin][k]])
                                script_ws = set([x["ws_url"] for x in v if "ws_url" in x])
                                desktop_repo_ws = set([x["ws_url"] for x in desktop_coins[coin][k] if "ws_url" in x])
                                needs_update = False

                                if not desktop_repo_electrums == script_electrums:
                                    needs_update = True
                                    errors["electrum_mismatch"] += 1
                                    electrums_not_in_desktop = desktop_repo_electrums - script_electrums
                                    electrums_not_in_output = script_electrums - desktop_repo_electrums
                                    print(colorize(f"{coin} has mismatch on {k}:", 'red'))
                                    if len(electrums_not_in_output):
                                        print(colorize(f"script_output is missing: {electrums_not_in_output}", 'yellow'))
                                    if len(electrums_not_in_desktop):
                                        print(colorize(f"desktop_repo is missing: {electrums_not_in_desktop}", 'blue'))

                                if not desktop_repo_ws == script_ws:
                                    needs_update = True
                                    errors["ws_mismatch"] += 1
                                    ws_not_in_desktop = desktop_repo_ws - script_ws
                                    ws_not_in_output = script_ws - desktop_repo_ws
                                    print(colorize(f"{coin} has mismatch on {k} (ws):", 'red'))
                                    if len(ws_not_in_output):
                                        print(colorize(f"script_output is missing: {ws_not_in_output}", 'yellow'))
                                    if len(ws_not_in_desktop):
                                        print(colorize(f"desktop_repo is missing: {ws_not_in_desktop}", 'blue'))
                                if needs_update:
                                    new_electrum_list = []
                                    for electrum in list(script_electrums.union(desktop_repo_electrums)):
                                        script_electrum = [i for i in v if i["url"] == electrum]
                                        desktop_electrum = [i for i in desktop_coins[coin][k] if i["url"] == electrum]
                                        if desktop_electrum and script_electrum:
                                            merged_electrum = dict(desktop_electrum[0])
                                            merged_electrum.update(script_electrum[0])
                                            new_electrum_list.append(merged_electrum)
                                        elif script_electrum:
                                            new_electrum_list.append(script_electrum[0])
                                        elif desktop_electrum:
                                            new_electrum_list.append(desktop_electrum[0])
                                    print("\n")
                                    print(coin)
                                    print(colorize(json.dumps(new_electrum_list, indent=4), 'green'))
                                    for i in new_electrum_list:
                                        if "contact" in i:
                                            del i["contact"]
                                    print("\n")
                                    print(coin)
                                    print(colorize(json.dumps(new_electrum_list, indent=4), 'blue'))
                                    print("\n")

                    except AssertionError as e:
                        if k == 'name':
                            errors["name_mismatch"] += 1
                            print(colorize(f"{coin} has mismatch on {k}: {v} (desktop_repo) != {desktop_coins[coin][k]} (script_output)", 'blue'))
                        elif k == 'explorer_url':
                            errors["explorer_mismatch"] += 1
                            print(colorize(f"{coin} has mismatch on {k}: {v} (desktop_repo) != {desktop_coins[coin][k]} (script_output)", 'yellow'))
                        else:
                            errors["value_mismatch"] += 1
                            print(colorize(f"{coin} has mismatch on {k}: {v} (desktop_repo) != {desktop_coins[coin][k]} (script_output)", 'magenta'))
                else:
                    if isinstance(v, bool):
                        pass
                    elif k in ["coingecko_id", "coinpaprika_id", "nomics_id", "forex_id"]:
                        print(f"{coin} is missing price API ID for {k} in script_output")
                        pass
                    elif k in ["explorer_tx_url", "explorer_address_url"]:
                        #print(f"{coin} is missing explorer suffix '{k}' in script_output")
                        pass
                    else:
                        errors["no_value"] += 1
                        print(colorize(f"{coin} has no value for {k} in script_output", "red"))

    total_errors = sum(list(errors.values()))
    print(f"\n{len(desktop_repo_coins)} desktop repo coins, {len(desktop_coins)} coins output")
    print(f"\n{errors} errors found! ({total_errors} total)")



if __name__ == "__main__":
    if len(sys.argv) > 1:
        valid_params = ["update_apis"]
        if sys.argv[1] not in valid_params:
            print(f"Invalid option, select from {valid_params}")
            sys.exit()
        if sys.argv[1] == "update_apis":
            get_api_ids_from_desktop()
    else:
        desktop_coins = parse_coins_repo()

        with open("desktop_coins.json", "w+") as f:
            json.dump(desktop_coins, f, indent=4)

        compare_output_vs_desktop_repo(desktop_coins)
