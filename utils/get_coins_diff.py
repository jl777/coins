#!/usr/bin/env python3
import argparse
import requests

'''
Use this script to determine which coins were added or removed between two commits.
To find the commit that matches app release dates, refer to
https://github.com/KomodoPlatform/coins/commits/master/utils/coins_config.json

You can use the full hash or the short hash (first 7 characters) of the commit.
'''

def get_coins_from_commit(commit: str, org: str = "komodoplatform", repo: str = "coins") -> set:
    url = build_coins_config_url(commit, org="komodoplatform", repo="coins")
    r = requests.get(url)
    try:
        return set(list(r.json().keys()))
    except Exception as e:
        print(f"{type(e)} error: {e}")
        return set()


def build_coins_config_url(commit, org="komodoplatform", repo="coins"):
    return "https://raw.githubusercontent.com/" + org + "/" + repo + "/" + commit + "/utils/coins_config.json"


def get_delisted_coins(old_coins, new_coins):
    return list(old_coins - new_coins)

def get_new_listed_coins(old_coins, new_coins):
    return list(new_coins - old_coins)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Returns the add/remove list of coins between two commits.')
    parser.add_argument('old_commit', type=str, help='Old commit hash')
    parser.add_argument('new_commit', type=str, help='New commit hash')
    # Parse the argument
    args = parser.parse_args()
    old_coins = get_coins_from_commit(args.old_commit)
    new_coins = get_coins_from_commit(args.new_commit)

    print(f"New coin listings: {get_new_listed_coins(old_coins, new_coins)}")
    print(f"Delisted coins: {get_delisted_coins(old_coins, new_coins)}")
