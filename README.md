
> NOTE
>
> The filename in each subdirectory needs to match the coin's symbol exactly, it is the unique field by which different coins are indexed. Please use .png files for icons

## About this repository

This repository is the coins database which is accessed by [AtomicDEX API](https://github.com/KomodoPlatform/atomicDEX-API/) and graphical applications like [AtomicDEX Mobile](https://github.com/KomodoPlatform/atomicDEX), [atomicDEX-Desktop](https://github.com/KomodoPlatform/atomicDEX-Desktop), DogeDEX etc. to enable coins for trading.

## Prerequisites for a coin to be compatible with AtomicDEX-API

### Bitcoin compatibles

```bash
estimatefee
getblock
getblockhash
getinfo
getrawtransaction
gettxout
importaddress
listunspent
listreceivedbyaddress
listtransactions
sendrawtransaction
```

### ERC20 tokens

- The token contract must have `approve` and `transferFrom` methods. Additionally, the `transfer` and `transferFrom` methods must return a boolean value (`true/false`) indicating whether a transfer was successful. This requirement is actually a part of the ERC20 standard, but many tokens seem to not follow it.

When submitting a pull request to add a coin to AtomicDEX-API, make sure you have completed this checklist:

## 0. The coin must have participated in a successful Atomic Swap using [AtomicDEX-API](https://github.com/KomodoPlatform/atomicDEX-API/)

When submitting your coin addition request, please submit the URLs of the 5 transactions (`takerfee sent`, `maker payment`, `taker payment` and `taker payment spent`, `maker payment spent`) produced by successful swap in a new file inside the [swaps directory](swaps), [example](swaps/BEER-ETOMIC.md). This means that, before going through the further steps and submitting the information to this coins database repo, you would have performed a successful atomic swap. The further steps explain the expected files/values to be submitted.

You can learn about performing an atomic swap from our documentation at [this link](https://developers.komodoplatform.com/basic-docs/atomicdex/atomicdex-tutorials/introduction-to-atomicdex.html)

Activating a coin: [https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/coin_activation.html](https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/coin_activation.html)

Walkthrough: [https://developers.komodoplatform.com/basic-docs/atomicdex/atomicdex-tutorials/atomicdex-walkthrough.html](https://developers.komodoplatform.com/basic-docs/atomicdex/atomicdex-tutorials/atomicdex-walkthrough.html)

If you have any questions, please ask in the `#support` channel in [our Discord server](https://komodoplatform.com/discord) or you can get help from the team at coinintegration@komodoplatform.com or partners@komodplatform.com .

## 1. Coin info added to `coins` file (Required)
You need the following info in JSON format added to the [coins](coins) file:

### Example 1 (UTXO coin)

```json
        {
                "coin": "LTC",
                "name": "litecoin",
                "fname": "Litecoin",
                "rpcport": 9332,
                "pubtype": 48,
                "p2shtype": 50,
                "wiftype": 176,
                "txfee": 0,
                "dust": 5460,
                "segwit": true,
                "mm2": 1,
                "required_confirmations": 2,
                "avg_blocktime": 2.5,
                "protocol": {
                        "type": "UTXO"
                }
        }
```

### Example 2 (KMD smartchain)

```json
        {
                "coin": "MCL",
                "asset": "MCL",
                "fname": "MarmaraCreditLoops",
                "rpcport": 33825,
                "txversion": 4,
                "overwintered": 1,
                "mm2": 1,
                "required_confirmations": 5,
                "requires_notarization": false,
                "avg_blocktime": 1,
                "protocol": {
                        "type": "UTXO"
                }
        }
```

### Example 3 (ERC20 token)

```json
        {
                "coin": "USDC-ERC20",
                "name": "usdc_erc20",
                "fname": "USD Coin",
                "rpcport": 80,
                "mm2": 1,
                "chain_id": 1,
                "required_confirmations": 3,
                "avg_blocktime": 0.25,
                "protocol": {
                        "type": "ERC20",
                        "protocol_data": {
                                "platform": "ETH",
                                "contract_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
                        }
                }
        }
```

### Example 4 (BEP20 token)

```json
        {
                "coin": "USDC-BEP20",
                "name": "usdc_bep20",
                "fname": "USD Coin",
                "rpcport": 80,
                "mm2": 1,
                "chain_id": 56,
                "avg_blocktime": 0.05,
                "required_confirmations": 3,
                "protocol": {
                        "type": "ERC20",
                        "protocol_data": {
                                "platform": "BNB",
                                "contract_address": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"
                        }
                }
        },
```

### Example 5 (QRC20 token)

```json
        {
                "coin": "QC",
                "name": "qtum",
                "fname": "Qcash",
                "rpcport": 3889,
                "pubtype": 58,
                "p2shtype": 50,
                "wiftype": 128,
                "segwit": true,
                "txfee": 0,
                "mm2": 1,
                "required_confirmations": 3,
                "mature_confirmations":500,
                "avg_blocktime": 2.133,
                "protocol": {
                        "type": "QRC20",
                        "protocol_data": {
                                "platform": "QTUM",
                                "contract_address": "0xf2033ede578e17fa6231047265010445bca8cf1c"
                        }
                }
        }
```

## General parameters

- `"coin"` must be coin ticker. If the coin is on more than one chain, please use `COIN-CHAIN` as ticker, eg `USDC-BEP20`. 
- `"fname"` must be coin's full name.
- `"mm2"` all the coins that were successfully atomic swapped through the AtomicDEX-API have this key set to `1` (you have to set this parameter to `1` in your local coins file when testing)
- `"required_confirmations"` the number of confirmations AtomicDEX will wait for during the swap. Default value is 1. WARNING, this setting affects the security of the atomic swap. 51% attacks (double spending) are a threat and have been succesfully conducted in the past. Read more about it [here](https://komodoplatform.com/51-attack-how-komodo-can-help-prevent-one/). You can find a collection of coins and the theoretical cost of a 51% attack [here](https://www.crypto51.app/). Please be aware that some of the coins supported by AtomicDEX are vulnerable to such attacks, so consider using higher values for them, especially when dealing with high amounts.
- `"requires_notarization"` tells AtomicDEX to wait for a notarization during the swap. This only works with dPoW coins and `"required_confirmations"` must be set to `2` or higher.
- `"decimals"` defines the number of digits after the decimal point that should be used to display the orderbook amounts, balance, and the value of inputs to be used in the case of order creation or a `withdraw` transaction. The default value used for a UTXO type coin (Bitcoin Protocol) is `8` and the default value used for a ERC20 Token is `18`. It is very important for this value to be set correctly. For example, if this value was set as `9` for BTC, a command to withdraw `1 BTC` tries to withdraw `10^9` satoshis of Bitcoin, i.e., `10 BTC`
- `"protocol"` contains the coin protocol `"type"` (UTXO, ETH, etc.) and specific protocol configuration - `"protocol_data"` object that can have arbitrary format. 
- `"orderbook_ticker"` - If set, coins with the same value will share the same orderbook. For example, if `BTC-Segwit` and `BTC-BEP20` are set with  `"orderbook_ticker":"BTC"` the same orderbook is returned for KMD/BTC, KMD/BTC-BEP20 and KMD/BTC-Segwit pairs. 

## Bitcoin Protocol specific JSON

- `"name"` must be coin's name, in all small letters. This is the value which is expected to be default data directory name for that coin. Example if coin's name is `litecoin` then it's expected data directory on Linux is `~/.litecoin/`, on Mac `~/Library/Applications Support/Litecoin/`, on Windows `%AppData%\Litecoin`. Please keep this key's value in small letters only.
- `"confpath"` must be ONLY used in case the expected data directory name of the coin/project is different to the `"name"`'s value, as explained in last point. Please refer to [Example 3](#example-3) for better understanding. Make sure to use the exact format for `confpath`. You don't need to change the word `USERHOME`, it remains as is. Make sure you have `/.` after `USERHOME`. And then the expected coin/project's data directory path and it's expected `.conf` file name.
- `"rpcport"` must be coin's default RPC port. It is expected that it doesn't conflict with any existing coin in the coins db.
- `"pubtype"`, `"p2shtype"`, and `"wiftype"` is the also very specific information about coin's parameters. This is specific to Bitcoin Protocol compatible coins only, and such information can be found in source code of the project. These parameters information can be expected in files like `src/init.cpp`, `src/base58.h`, and `src/chainparamsbase.h` if the project is following the **bitcoin** source code directory/files structure. If the parameters info is unclear then please have these confirmed by that coin/project's developers and make sure it's correct information.
- `"txfee"` is a value of default transactions fee, which must be specified in satoshies unit. AtomicDEX uses this as the default transaction fee value when making atomic swaps transactions. If set to `0`, AtomicDEX will use a dynamic fee based on output from `estimatesmartfee`.
- `"overwintered"` must be `1` if Overwinter upgrade was activated for the coin.
- `"taddr"` is only relevant for coins that forked the Zcash protocol and have both transparent addresses and z-addresses. The value to be set for this key can be found from the file `src/chainparams.cpp` of the coin's source code and it is the first value present in both `base58Prefixes[PUBKEY_ADDRESS]` and `base58Prefixes[SCRIPT_ADDRESS]`. But it has to be converted to decimal from HEX. So if `base58Prefixes[PUBKEY_ADDRESS]` = `{0x1C,0xB8}` , the `taddr` is `0x1C` coverted to decimal. As 0x1C in HEX = 28 in decimal, the entry in the json will be `"taddr" : 28`
- `force_min_relay_fee` - if this key is set to true for coins with dynamic fees, when a new transaction is generated, AtomicDEX-API will check whether the total fee set (`sat * tx size`) is lower than relay fee and will use the relay fee instead.
- `mtp_block_count` - number of blocks to be used for the calculation of `median time past`. Must be greater than `0`. Default value is `11`. While this parameter is applicable only in the case of KMD reward calculation for now, it will be used for calculating locktimes to be set for the atomic swap refund transactions. Can be ignored for most coins for now.
- `estimate_fee_mode` - sets the fee mode for the `estimatesmartfee` call. Supported values are: `ECONOMICAL`,`CONSERVATIVE`, `UNSET`. Please note that some coins may not support some of these modes. Makes no effect for coins that do not have the `estimatesmartfee` RPC.
- `address_format` - defines whether to use the standard bitcoin address format or the cash address format for BCH. More formats may be added in the future. Possible values as of now: `"address_format":{"format":"standard"}` to set the standard BTC/UTXO address format. `"address_format":{"format":"cashaddress","network":"NETWORK_ID"}` to use BCH specific address format. `NETWORK_ID` can be: `bitcoincash` for BCH mainnet, `bchtest` for BCH testnet and `bchreg` for BCH regtest.
- `isPoS` - whether the coin uses proof of stake. This key decides whether the transactions created have the `nTime` field. Can be `0` or `1`.
- `segwit` - is a boolean value, if set to true, AtomicDEX-API will allow withdrawal to `P2SH` addresses. Will possibly mean full segwit support in the future.
- `version_group_id` - sets the `version_group_id` used by Zcash (and its forks') transactions. Determined automatically by tx version and `overwintered` if not set.
- `consensus_branch_id` - sets the `consensus_branch_id` used in Zcash (and its forks') transactions' signature hash calculation. Determined automatically by tx version and `overwintered` if not set.
- `mature_confirmations` - number of blockchain confirmations required for coinbase output to be considered mature (spendable).

## Ethereum Protocol specific JSON

- Ethereum protocol specific coin/project add request are the simplest. `"coin"`, `"name"`, and `"fname"` information is same as explained in bitcoin protocol specific json section.
- `chain_id` - ID of the chain, see [Chainlist](https://chainlist.org/)
- Protocol `"type"` field: `"ETH"` or `"ERC20"`
- Protocol `"protocol_data"` field (ERC20 only): `"platform"` - `"ETH"`, `"ETC"` or other Ethereum forks. `"contract_address"` - ERC20 token [checksummed](https://coincodex.com/article/2078/ethereum-address-checksum-explained/) smart contract address.

## QRC20 Protocol specific JSON
- Supports all fields of UTXO specific config.
- Protocol `"type"` field: `"QRC20"`.
- Protocol `"protocol_data"` field: `"platform"` - `"QTUM"` or QTUM forks. `"contract_address"` - QRC20 token smart contract address.

## 2. Icon file (Required)

- The icon file is required.
- Icon must be a .png format file.
- Dimentions of icon file is 82x82 pixels.
- Icon file name MUST be in **small letters**.
- Icon file location is [icons](icons) directory.

## 3. Explorer URL (Required)

- Explorer file name must be coin's ticker name matching the `"coin"` value as specified in [coins](coins) file.
- Explorer file name must not have any file extension. It is a file without any `.` extension.
- Explorer file name must be in all **capital** letters.
- It must have a valid JSON array with at least one Explorer URL in it. It's better if there are more than one explorer URLs in this JSON array. Example: `["http://example1.com/tx/","http://example2.com/tx/"]`.
- The URL of Explorer must be pointing to the transactions URL. Check BTC file for an example: [explorers/BTC](explorers/BTC), which has `["https://www.blocktrail.com/BTC/tx/"]`. This explorers URL is used to link to the transactions like this [example link](https://www.blocktrail.com/BTC/tx/5268d045196e940ca8ba53b442c38a0f8c159002c912f8427239153dce984cc3/) in GUIs. Make sure this URL ends with `/`.

## 4. Electrum Servers (Optional; Required for listing in Mobile GUIs)

- Electrum file name must be coin's ticker name matching the `"coin"` value as specified in [coins](coins) file.
- Electrum file name must not have any file extension. It is a file without any `.` extension.
- Electrum file name must be all in **capital** letters.
- It must be a valid JSON format as shown in the following example:

```JSON
[
  {
    "url": "nmc.bitcoins.sk:50002",
    "protocol": "SSL",
    "disable_cert_verification": true,
    "contact": [
      {"email": "electrum1_admin_email@example.com"},
      {"matrix": "@electrum1_admin:matrix.org"},
      {"skype": "example_username"},
      {"twitter": "example_username"},
      {"reddit": "example_username"},
      {"github": "example_username"},
      {"keybaseio": "example_username"}
    ]
  },
  {
    "url": "electrum-nmc.le-space.de:50002",
    "protocol": "SSL",
    "disable_cert_verification": false,
    "contact": [
      {"email": "electrum2_admin_email@example.com"}
    ]
  }
]
```

- Details of at least 2 Electrum servers must be provided.
- Protocol can be "SSL" or "TCP".
- Contact information must be provided in case the server admin needs to be contacted in emergency situations. It can be any contact information out of the examples provided. Or may be add your own service/contact information as it suites you.
- The address and port of electrum server are required. The address of electrum server can either be a DNS or an IP address.

## 5. Ethereum info file (Required for ETH/ERC20)

- File name must be coin's ticker name matching the `"coin"` value as specified in [coins](coins) file.
- File name must not have any file extension. It is a file without any `.` extension.
- File name must be all in **capital** letters.
- It must be a valid JSON format as shown in the following example:

```JSON
{
  "swap_contract_address":"0x8500AFc0bc5214728082163326C2FF0C73f4a871",
  "rpc_nodes": [
      {
        "url":"http://ethnode.com:8545",
        "contact": [
          {"email": "ethnode_admin_email@example.com"},
          {"matrix": "@ethnode_admin:matrix.org"},
          {"skype": "example_username"},
          {"twitter": "example_username"},
          {"reddit": "example_username"},
          {"github": "example_username"},
          {"keybaseio": "example_username"}
        ]
      },
      {
        "url":"http://ethnode2.com:8545",
        "contact": [
          {"email": "ethnode2_admin_email@example.com"}
        ]
      }
  ]
}
```

- Swap contract address must be the address of [etomic swap smart contract](https://github.com/artemii235/etomic-swap) deployed to ETH network, [example](https://etherscan.io/address/0x8500afc0bc5214728082163326c2ff0c73f4a871).
- At least minimum 2 or more URLs of RPC nodes must be provided.
- Contact information must be provided in case the server admin needs to be contacted in urgent cases. It can be any contact information out of the examples provided. Or may be add your own service/contact information as suites you.
- The RPC node URL can either be a DNS or an IP address with port.
