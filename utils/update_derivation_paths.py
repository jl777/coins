#!/usr/bin/env python3
import json

with open('../coins', "r") as f:
    coins = json.load(f)

with open('protocol_derivation_paths.json', "r") as f:
    paths = json.load(f)

not_processed = {}
segwit_coins = []

for i in coins:
    split = i["coin"].split("-")
    if "derivation_path" not in i:
        if "sign_message_prefix" in i:
            if i["sign_message_prefix"] == "Komodo Signed Message:\n":
                i.update({"derivation_path": paths["KMD"]})

        elif len(split) == 2:
            proto = split[1]
            if proto in paths.keys():
                i.update({"derivation_path": paths[proto]})
            elif proto == "segwit":
                segwit_coins.append(i["coin"])
            else:
                if proto not in not_processed:
                    not_processed.update({proto:[]})
                not_processed[proto].append(i["coin"])

        else:
            if "protocol_data" in i["protocol"]:
                if "platform" in i["protocol"]["protocol_data"]:
                    proto = i["protocol"]["protocol_data"]["platform"]
                    if proto == "ETH":
                        proto = "ERC20"
                    elif proto == "BNB":
                        proto = "BEP20"
                    elif proto == "QTUM":
                        proto = "QRC20"
                    if proto in paths.keys():
                        i.update({"derivation_path": paths[proto]})
                        print(f"{i['coin']} proto suffix needs update with -{proto}")
                    else:
                        print(f"{i['coin']} proto {proto} unrecognised")
                        if proto not in not_processed:
                            not_processed.update({proto:[]})
                        not_processed[proto].append(i["coin"])
            else:
                proto = i["protocol"]["type"]
                if proto not in not_processed:
                    not_processed.update({proto:[]})
                not_processed[proto].append(i["coin"])
                print(f"{i['coin']} with proto {proto} has no derivation_path info")

    else:
        if "protocol_data" in i["protocol"]:
            if "platform" in i["protocol"]["protocol_data"]:
                proto = i["protocol"]["protocol_data"]["platform"]
                if proto == "ETH":
                    proto = "ERC20"
                elif proto == "BNB":
                    proto = "BEP20"
                elif proto == "QTUM":
                    proto = "QRC20"
                if proto in paths.keys():
                    if paths[proto] != i["derivation_path"]:
                        print(f"Path mismatch for {i['coin']}")

for coin in segwit_coins:
    path = ""
    ticker = coin.replace("-segwit", "")
    for i in coins:
        if i["coin"] == ticker:
            proto = i['protocol']['type']
            if proto in ["UTXO", "QTUM"]:
                if 'derivation_path' in i:
                    path = i['derivation_path']
    for i in coins:
        if i["coin"] == coin:
            if path != "":
                i.update({"derivation_path": path})
            else:
                print(f"Unable to determine path for {coin} (segwit)")




print(f'The following coins were not processed')
for proto in not_processed:
    print(f"{proto}: {not_processed[proto]}")

with open("../coins", 'w') as f:
    json.dump(coins, f, indent=2)