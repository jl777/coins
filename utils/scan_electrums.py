#!/usr/bin/env python3
import os
import ssl
import json
import time
import socket
import requests
import threading

ignore_list = []
passed_electrums = {}
passed_electrums_ssl = {}
failed_electrums = {}
failed_electrums_ssl = {}
socket.setdefaulttimeout(10)
os.chdir(os.path.abspath(os.path.dirname(__file__)))


def colorize(string, color):
    colors = {
            'red':'\033[31m',
            'green':'\033[32m'
    }
    if color not in colors:
            return str(string)
    else:
            return colors[color] + str(string) + '\033[0m'


def get_from_electrum(url, port, method, params=None):
    if params:
        params = [params] if type(params) is not list else params
    try:
        with socket.create_connection((url, port)) as sock:
            payload = {"id": 0, "method": method}
            if params:
                payload.update({"params": params})
            sock.send(json.dumps(payload).encode() + b'\n')
            time.sleep(3)
            resp = sock.recv(999999)[:-1].decode()
            return resp
    except Exception as e:
        return e


def get_from_electrum_ssl(url, port, method, params=None):
    if params:
        params = [params] if type(params) is not list else params
    context = ssl.SSLContext(verify_mode=ssl.CERT_NONE)
    try:
        with socket.create_connection((url, port)) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                payload = {"id": 0, "method": method}
                if params:
                    payload.update({"params": params})
                ssock.send(json.dumps(payload).encode() + b'\n')
                time.sleep(3)
                resp = ssock.recv(999999)[:-1].decode()
                return resp
    except Exception as e:
        return e


class electrum_thread(threading.Thread):
    def __init__(self, coin, ip, port, method, params=None, is_ssl=False):
        threading.Thread.__init__(self)
        self.coin = coin
        self.ip = ip
        self.port = port
        self.method = method
        self.params = params
        self.is_ssl = is_ssl
    def run(self):
        if self.is_ssl:
            thread_electrum_ssl(self.coin, self.ip, self.port, self.method, self.params)
        else:
            thread_electrum(self.coin, self.ip, self.port, self.method, self.params)


def thread_electrum(coin, ip, port, method, params):
    resp = get_from_electrum(ip, port, method, params)
    try:
        resp_json = json.loads(resp)['result']
        # print(resp_json)
        print(colorize(f"{coin} {ip}:{port} OK!", 'green'))
        if coin not in passed_electrums:
            passed_electrums.update({coin:[]})
        passed_electrums[coin].append(f"{ip}:{port}")

    except Exception as e:
        if str(resp).find('{"jsonrpc": "2.0"') > -1:
            if coin not in passed_electrums:
                passed_electrums.update({coin:[]})
            passed_electrums[coin].append(f"{ip}:{port}")
            print(colorize(f"{coin} {ip}:{port} OK!", 'green'))
            return
        if coin not in failed_electrums:
            failed_electrums.update({coin:{}})
        failed_electrums[coin].update({f"{ip}:{port}": f"{resp}"})
        print(colorize(f"{coin} {ip}:{port} Failed! {e} | {resp}", 'red'))


def thread_electrum_ssl(coin, ip, port, method, params):
    resp = get_from_electrum_ssl(ip, port, method, params)
    try:
        resp_json = json.loads(resp)['result']
        print(colorize(f"{coin} {ip}:{port} OK!", 'green'))
        if coin not in passed_electrums_ssl:
            passed_electrums_ssl.update({coin:[]})
        passed_electrums_ssl[coin].append(f"{ip}:{port}")

    except Exception as e:
        if str(resp).find('{"jsonrpc": "2.0"') > -1:
            if coin not in passed_electrums_ssl:
                passed_electrums_ssl.update({coin:[]})
            passed_electrums_ssl[coin].append(f"{ip}:{port}")
            print(colorize(f"{coin} {ip}:{port} OK!", 'green'))
            return
        if coin not in failed_electrums_ssl:
            failed_electrums_ssl.update({coin:{}})
        failed_electrums_ssl[coin].update({f"{ip}:{port}": f"{resp}"})
        print(colorize(f"{coin} {ip}:{port} Failed! {e} | {resp}", 'red'))


def scan_electrums(electrum_dict):
    thread_list = []
    ssl_list = []
    non_ssl_list = []
    for coin in electrum_dict:
        for electrum in electrum_dict[coin]:
            url, port = electrum["url"].split(":")
            if "protocol" in electrum:
                if electrum["protocol"] == "SSL":
                    ssl_list.append(coin)
                    thread_list.append(electrum_thread(coin, url, port, "blockchain.block.headers", [1,2], True))
                    continue
            non_ssl_list.append(coin)
            thread_list.append(electrum_thread(coin, url, port, "blockchain.block.headers", [1,2]))

    for thread in thread_list:
        thread.start()
        time.sleep(0.1)
    return set(ssl_list), set(non_ssl_list)


def get_repo_electrums():
    electrum_coins = os.listdir("../electrums")
    repo_electrums = {}
    for coin in electrum_coins:
        with open(f"../electrums/{coin}", "r") as f:
            electrums = json.load(f)
            repo_electrums.update({coin: electrums})
    return repo_electrums


def get_electrums_report():

    electrum_dict = get_repo_electrums()
    electrum_coins_ssl, electrum_coins = scan_electrums(electrum_dict)

    i = 0
    while True:
        electrums_set = set(list(passed_electrums.keys()) + list(failed_electrums.keys())) - set(ignore_list)
        electrums_ssl_set = set(list(passed_electrums_ssl.keys()) + list(failed_electrums_ssl.keys())) - set(ignore_list)
        electrums_pct = round(len(electrums_set) / len(electrum_coins) * 100, 2)
        electrums_ssl_pct = round(len(electrums_ssl_set) / len(electrum_coins_ssl) * 100, 2)
        print(f"Scan progress: {electrums_pct}% electrums,  {electrums_ssl_pct}% electrums_ssl, ")
        if electrums_set == electrum_coins:
            if electrums_ssl_set == electrum_coins_ssl:
                break
        if i > 60:
            print("Loop expired incomplete after 60 iterations.")
            break
        i += 1
        time.sleep(1)

    results = {
        "passed": passed_electrums,
        "passed_ssl": passed_electrums_ssl,
        "failed": failed_electrums,
        "failed_ssl": failed_electrums_ssl
    }

    for coin in list(electrums_ssl_set.union(electrums_set)):
        if coin in passed_electrums: passed = len(passed_electrums[coin])
        else: passed =  0
        if coin in passed_electrums_ssl: passed_ssl = len(passed_electrums_ssl[coin])
        else: passed_ssl = 0
        if coin in failed_electrums: failed = len(failed_electrums[coin])
        else: failed = 0
        if coin in failed_electrums_ssl: failed_ssl = len(failed_electrums_ssl[coin])
        else: failed_ssl = 0
        results.update({
            coin: {
                "passed": passed + passed_ssl,
                "failed": failed + failed_ssl
            }
        })

    with open("electrum_scan_report.json", "w+") as f:
        f.write(json.dumps(results, indent=4))

    # print(json.dumps(results, indent=4))

if __name__ == '__main__':
    get_electrums_report()