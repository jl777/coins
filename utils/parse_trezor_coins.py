#!/usr/bin/env python3
import requests
import json

with open('../coins', 'r') as f:
	coins_data = json.load(f)


trezor_data = requests.get("https://raw.githubusercontent.com/trezor/trezor-common/master/defs/coins_details.json").json()
clean_trezor_data = {}

coins_tickers = [i['coin'] for i in coins_data]
trezor_tickers = [i.split(":")[1] for i in list(trezor_data['coins'].keys())]

for i in trezor_data['coins']:
	split = i.split(":")
	clean_ticker = None
	if len(split) == 2:
		if split[0] in ["bitcoin", "eth"]:
			clean_ticker = split[1]
	else:
		if split[0] == "erc20":
			if split[1] == "eth":
				clean_ticker = f"{split[2]}-ERC20"

	if clean_ticker:
		if clean_ticker in coins_tickers:
			print(f"{i} {clean_ticker} found in coins file! Trezor_name is {trezor_data['coins'][i]['name']}")
			if clean_ticker not in clean_trezor_data:
				clean_trezor_data.update({
					clean_ticker: trezor_data['coins'][i]
				})
			else:
				print(f"{i} already in dict!")

for i in trezor_data['coins']:
	split = i.split(":")
	clean_ticker = None
	if len(split) == 2:
		if split[0] in ["bitcoin"]:
			clean_ticker = f"{split[1]}-segwit"
	if clean_ticker:
		if clean_ticker in coins_tickers:
			print(f"{i} {clean_ticker} found in coins file! Trezor_name is {trezor_data['coins'][i]['name']}")
			if clean_ticker not in clean_trezor_data:
				clean_trezor_data.update({
					clean_ticker: trezor_data['coins'][i]
				})
			else:
				print(f"{i} already in dict!")

for ticker in clean_trezor_data:
	for i in coins_data:
		if ticker == i["coin"]:
			i.update({
				"trezor_coin": clean_trezor_data[ticker]["name"],
			})

			if "links" in clean_trezor_data[ticker]:
				i.update({
					"links": {}
				})
				for link in clean_trezor_data[ticker]["links"]:
					i["links"].update({
						link.lower(): clean_trezor_data[ticker]["links"][link]
					})
			break

with open('../coins', 'w') as f:
	json.dump(coins_data, f, indent=2)
