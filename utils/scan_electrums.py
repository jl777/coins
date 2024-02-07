#!/usr/bin/env python3
import os
import sys
import ssl
import json
import time
import socket
import threading
import asyncio
import websockets


ignore_list = []
passed_electrums = {}
failed_electrums = {}
passed_electrums_ssl = {}
failed_electrums_ssl = {}
passed_electrums_wss = {}
failed_electrums_wss = {}
socket.setdefaulttimeout(10)
script_path = os.path.abspath(os.path.dirname(__file__))
repo_path = script_path.replace("/utils", "")
os.chdir(script_path)


def colorize(string, color):
    colors = {
            'red':'\033[31m',
            'blue':"\x1b[38;2;59;142;200m",
            'green':'\033[32m'
    }
    if color not in colors:
            return str(string)
    else:
            return colors[color] + str(string) + '\033[0m'


def get_from_electrum(url, port, method, params=None):
    if 'cipig.net' in url:
        return '{"result": "cipig.net is always welcome."}'
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
    if 'cipig.net' in url:
        return '{"result": "cipig.net is always welcome."}'
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


def get_from_electrum_wss(url, port, method, params=None):
    if 'cipig.net' in url:
        return '{"result": "cipig.net is always welcome."}'
    
    if params:
        params = [params] if type(params) is not list else params
    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        async def connect_and_query():
            async with websockets.connect(f"wss://{url}:{port}", ssl=ssl_context, timeout=10) as websocket:
                payload = {"id": 0, "method": method}
                if params:
                    payload.update({"params": params})
                await websocket.send(json.dumps(payload))
                await asyncio.sleep(3)
                resp = await asyncio.wait_for(websocket.recv(), timeout=7)
                return resp
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(connect_and_query())
        return response
    except Exception as e:
        return e


class scan_thread(threading.Thread):
    def __init__(self, coin, ip, port, method, params=None, protocol='tcp'):
        threading.Thread.__init__(self)
        self.coin = coin
        self.ip = ip
        self.port = port
        self.method = method
        self.params = params
        self.protocol = protocol
    def run(self):
        if self.protocol == "ssl":
            thread_electrum_ssl(self.coin, self.ip, self.port, self.method, self.params)
        elif self.protocol == "tcp":
            thread_electrum(self.coin, self.ip, self.port, self.method, self.params)
        elif self.protocol == "wss":
            thread_electrum_wss(self.coin, self.ip, self.port, self.method, self.params)


def thread_electrum_wss(coin, ip, port, method, params):
    resp = get_from_electrum_wss(ip, port, method, params)
    try:
        resp_json = json.loads(resp)['result']
        print(colorize(f"{coin} {ip}:{port} OK!", 'blue'))
        if coin not in passed_electrums_wss:
            passed_electrums_wss.update({coin:[]})
        passed_electrums_wss[coin].append(f"{ip}:{port}")

    except Exception as e:
        if str(resp).find('{"jsonrpc": "2.0"') > -1:
            if coin not in passed_electrums_wss:
                passed_electrums_wss.update({coin:[]})
            passed_electrums_wss[coin].append(f"{ip}:{port}")
            print(colorize(f"{coin} {ip}:{port} OK!", 'green'))
            return
        if coin not in failed_electrums_wss:
            failed_electrums_wss.update({coin:{}})
        failed_electrums_wss[coin].update({f"{ip}:{port}": f"{resp}"})
        print(colorize(f"{coin} {ip}:{port} Failed! {e} | {resp}", 'red'))



def thread_electrum(coin, ip, port, method, params):
    resp = get_from_electrum(ip, port, method, params)
    try:
        resp_json = json.loads(resp)['result']
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
    wss_list = []
    ssl_list = []
    non_ssl_list = []

    for coin in electrum_dict:
        for electrum in electrum_dict[coin]:
            if "ws_url" in electrum:
                url, port = electrum["ws_url"].split(":")
                wss_list.append(coin)
                thread_list.append(scan_thread(coin, url, port, "blockchain.block.headers", [1,2], "wss"))
                
            if 'url' in electrum:
                url, port = electrum["url"].split(":")
                if "protocol" in electrum:
                    if electrum["protocol"] == "SSL":
                        ssl_list.append(coin)
                        thread_list.append(scan_thread(coin, url, port, "blockchain.block.headers", [1,2], "ssl"))
                        continue
                non_ssl_list.append(coin)
                thread_list.append(scan_thread(coin, url, port, "blockchain.block.headers", [1,2], "tcp"))

    for thread in thread_list:
        thread.start()
        time.sleep(0.1)
    return set(ssl_list), set(non_ssl_list), set(wss_list)


def get_repo_electrums():
    electrum_coins = [f for f in os.listdir(f"{repo_path}/electrums") if os.path.isfile(f"{repo_path}/electrums/{f}")]
    repo_electrums = {}
    for coin in electrum_coins:
        try:
            with open(f"../electrums/{coin}", "r") as f:
                electrums = json.load(f)
                repo_electrums.update({coin: electrums})
        except json.decoder.JSONDecodeError:
            print(f"{coin} electrums failed to parse, exiting.")
            sys.exit(1)
    return repo_electrums


def get_existing_report():
    if os.path.exists("electrum_scan_report.json"):
        with open("electrum_scan_report.json", "r") as f:
            return json.load(f)
    return {}


def get_last_connection(report, coin, protocol, server):
    try:
        return report[coin][protocol][server]["last_connection"]
    except KeyError:
        return 0
    except TypeError:
        return 0



def get_electrums_report():
    current_time = int(time.time())
    existing_report = get_existing_report()
    electrum_dict = get_repo_electrums()
    electrum_coins_ssl, electrum_coins, electrum_coins_wss = scan_electrums(electrum_dict)

    i = 0
    while True:
        electrums_set = set(list(passed_electrums.keys()) + list(failed_electrums.keys())) - set(ignore_list)
        electrums_ssl_set = set(list(passed_electrums_ssl.keys()) + list(failed_electrums_ssl.keys())) - set(ignore_list)
        electrums_wss_set = set(list(passed_electrums_wss.keys()) + list(failed_electrums_wss.keys())) - set(ignore_list)
        electrums_pct = round(len(electrums_set) / len(electrum_coins) * 100, 2)
        electrums_ssl_pct = round(len(electrums_ssl_set) / len(electrum_coins_ssl) * 100, 2)
        electrums_wss_pct = round(len(electrums_wss_set) / len(electrum_coins_wss) * 100, 2)
        print(f"Scan progress: {electrums_pct}% electrums,  {electrums_ssl_pct}% electrums_ssl,  {electrums_wss_pct}% electrums_wss ")
        if electrums_set == electrum_coins:
            if electrums_ssl_set == electrum_coins_ssl:
                if electrums_wss_set == electrum_coins_wss:
                    break
        if i > 10:
            print("Loop expired incomplete after 60 iterations.")
            break
        i += 1
        time.sleep(1)

    results = {}

    all_electrums = list(electrums_ssl_set.union(electrums_set).union(electrums_wss_set))
    all_electrums.sort()
    for coin in all_electrums:
        if coin in passed_electrums: passed = len(passed_electrums[coin])
        else: passed =  0
        if coin in passed_electrums_ssl: passed_ssl = len(passed_electrums_ssl[coin])
        else: passed_ssl = 0
        if coin in passed_electrums_wss: passed_wss = len(passed_electrums_wss[coin])
        else: passed_wss = 0
        if coin in failed_electrums: failed = len(failed_electrums[coin])
        else: failed = 0
        if coin in failed_electrums_ssl: failed_ssl = len(failed_electrums_ssl[coin])
        else: failed_ssl = 0
        if coin in failed_electrums_wss: failed_wss = len(failed_electrums_wss[coin])
        else: failed_wss = 0
        results.update({
            coin: {
                "electrums_total_all": passed + failed + passed_ssl + failed_ssl + passed_wss + failed_wss,
                "electrums_working_all": passed + passed_ssl + passed_wss,
                "electrums_total_tcp": passed + failed,
                "electrums_working_tcp": passed,
                "electrums_total_ssl": passed_ssl + failed_ssl,
                "electrums_working_ssl": passed_ssl,
                "electrums_total_wss": passed_wss + failed_wss,
                "electrums_working_wss": passed_wss,
                "tcp": {},
                "ssl": {},
                "wss": {}
            }
        })

        if coin in passed_electrums:
            x = list(passed_electrums[coin])
            x.sort()
            for i in x:
                results[coin]["tcp"].update({
                    i: {
                        "last_connection": current_time,
                        "result": "Passed"
                    }
                })

        if coin in failed_electrums:
            x = list(failed_electrums[coin].keys())
            x.sort()
            for i in x:
                results[coin]["tcp"].update({
                    i: {
                        "last_connection": get_last_connection(existing_report, coin, "tcp", i),
                        "result": failed_electrums[coin][i]
                    }
                })

        if coin in passed_electrums_ssl:
            x = list(passed_electrums_ssl[coin])
            x.sort()
            for i in x:
                results[coin]["ssl"].update({
                    i: {
                        "last_connection": current_time,
                        "result": "Passed"
                    }
                })

        if coin in failed_electrums_ssl:
            x = list(failed_electrums_ssl[coin].keys())
            x.sort()
            for i in x:
                results[coin]["ssl"].update({
                    i: {
                        "last_connection": get_last_connection(existing_report, coin, "ssl", i),
                        "result": failed_electrums_ssl[coin][i]
                    }
                })

        if coin in passed_electrums_wss:
            x = list(passed_electrums_wss[coin])
            x.sort()
            for i in x:
                results[coin]["wss"].update({
                    i: {
                        "last_connection": current_time,
                        "result": "Passed"
                    }
                })

        if coin in failed_electrums_wss:
            x = list(failed_electrums_wss[coin].keys())
            x.sort()
            for i in x:
                results[coin]["wss"].update({
                    i: {
                        "last_connection": get_last_connection(existing_report, coin, "wss", i),
                        "result": failed_electrums_wss[coin][i]
                    }
                })

    with open("electrum_scan_report.json", "w+") as f:
        f.write(json.dumps(results, indent=4))
    
    # print(json.dumps(results, indent=4))

if __name__ == '__main__':
    get_electrums_report()
