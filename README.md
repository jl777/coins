
NOTE: The filename in each subdirectory needs to match the coin's symbol exactly, it is the unique field by which different coins are indexed. Please use .png files for icons

### About this repository
This repository is the coins database which is accessed by [AtomicDEX API](https://github.com/KomodoPlatform/atomicDEX-API/) and graphical applications like [AtomicDEX Mobile](https://github.com/KomodoPlatform/atomicDEX), HyperDEX etc. to enable coins for trading.

When submitting a pull request to add a coin, make sure you have completed this checklist:

### 0. The coin must have participated in a successful Atomic Swap using [AtomicDEX](https://github.com/KomodoPlatform/atomicDEX-API/)
When submitting your coin add request please post the 5 transactions URLs produced by successful swap in separate file inside [swaps dir](swaps), [example](swaps/BEER-ETOMIC.md). This means that before submitting the further steps information to this coins database repo, you would have performed an atomic swap, and the further steps explains the expected files/values to be submitted to this database repo.

You can learn about performing an atomic swap from our documentation at [this link](https://developers.komodoplatform.com/basic-docs/atomicdex/atomicdex-tutorials/introduction-to-atomicdex.html)

Or you can contact the team at coinintegration@komodoplatform.com or one of the service providers listed at [https://komodoplatform.com/ecosystem/#service-providers](https://komodoplatform.com/ecosystem/#service-providers) to get help if required.

### 1. Coin info added to `coins` file (Required)
You need the following info in JSON format added to the [coins](coins) file:

```shell
# Example 1
  {
    "coin": "LTC",
    "name": "litecoin",
    "fname": "Litecoin",
    "rpcport": 9332,
    "pubtype": 48,
    "p2shtype": 50,
    "wiftype": 176,
    "txfee": 10000,
    "segwit": true,
    "mm2": 1,
    "required_confirmations": 2
  }

# Example 2
  {
    "coin": "RFOX",
    "asset": "RFOX",
    "fname": "RedFOX",
    "rpcport": 32269,
    "txversion": 4,
    "overwintered": 1,
    "mm2": 1,
    "required_confirmations": 2,
    "requires_notarization": true
  }

# Example 3
  {
    "coin": "ECA",
    "name": "electra",
    "fname": "Electra",
    "rpcport": 5788,
    "pubtype": 33,
    "p2shtype": 40,
    "wiftype": 161,
    "txfee": 10000,
    "txversion": 7,
    "mm2":1,
    "confpath": "USERHOME/.electra/Electra.conf",
    "required_confirmations": 10
  }

# Example 4
  {
    "coin": "BAT",
    "name": "basic-attention-token",
    "fname": "Basic Attention Token",
    "etomic": "0x0D8775F648430679A709E98d2b0Cb6250d2887EF",
    "rpcport": 80,
    "mm2": 1,
    "required_confirmations": 3
  }
```

#### General parameters

`"mm2"` add this param if coin is confirmed working with AtomicDEX (successful swap is made).

`"required_confirmations"` the number of confirmations AtomicDEX will wait for during the swap. Default value is 1. WARNING, this setting affects the security of the atomic swap. 51% attacks (double spending) are a threat and have been succesfully conducted in the past. Read more about it [here](https://komodoplatform.com/51-attack-how-komodo-can-help-prevent-one/). You can find a collection of coins and the theoretical cost of a 51% attack [here](https://www.crypto51.app/). Please be aware that some of the coins supported by AtomicDEX are vulnerable to such attacks, so consider using higher values for them, especially when dealing with high amounts.

`"requires_notarization"` tells AtomicDEX to wait for a notarization during the swap. This only works with dPoW coins and `"required_confirmations"` must be set to `2` or higher.


#### Bitcoin Protocol specific JSON

`"coin"` must be coin ticker.

`"name"` must be coin's name, in all small letters. This is the value which is expected to be default data directory name for that coin. Example if coin's name is `litecoin` then it's expected data directory on Linux is `~/.litecoin/`, on Mac `~/Library/Applications Support/Litecoin/`, on Windows `%AppData%\Litecoin`. Please keep this key's value in small letters only.

`"confpath"` must be ONLY used in case the expected data directory name of the coin/project is different to the `"name"`'s value, as explained in last point. Please refer to Example 2 for better understanding. Make sure to use the exact format for `confpath`. You don't need to change the word `USERHOME`, it remains as is. Make sure you have `/.` after `USERHOME`. And then the expected coin/project's data directory path and it's expected `.conf` file name.

`"fname"` must be coin's full name.

`"rpcport"` must be coin's default RPC port. It is expected that it doesn't conflict with any existing coin in the coins db.

`"pubtype"`, `"p2shtype"`, and `"wiftype"` is the also very specific information about coin's parameters. This is specific to Bitcoin Protocol compatible coins only, and such information can be found in source code of the project. These parameters information can be expected in files like `src/init.cpp`, `src/base58.h`, and `src/chainparamsbase.h` if the project is following the **bitcoin** source code directory/files structure. If the parameters info is unclear then please have these confirmed by that coin/project's developers and make sure it's correct information.

`"txfee"` is a value of default transactions fee, which must be specified in satoshies unit. AtomicDEX uses this as the default transaction fee value when making atomic swaps transactions. If set to `0`, AtomicDEX will use a dynamic fee based on output from `estimatesmartfee`.

`"overwintered"` must be `1` if Overwinter upgrade was activated for the coin.


#### Ethereum Protocol specific JSON

Ethereum protocol specific coin/project add request are the most simplest. `"coin"`, `"name"`, and `"fname"` information is same as explained in bitcoin protocol specific json section.

`"rpcport"` must remain default for all ERC20 token/coins. Make sure its only specified as `80`.

`"etomic"` must be the ERC20 token/coin's [checksummed](https://coincodex.com/article/2078/ethereum-address-checksum-explained/) smart contract address.


### 2. Icon file (Required)
- The icon file is required.
- Icon must be a .png format file.
- Dimentions of icon file is 82x82 pixels.
- Icon file name MUST be in **small letters**.
- Icon file location is [icons](icons) directory.


### 3. Explorer URL (Required)
- Explorer file name must be coin's ticker name matching the `"coin"` value as specified in [coins](coins) file.
- Explorer file name must not have any file extension. It is a file without any `.` extension.
- Explorer file name must be all in **capital** letters.
- It must have a valid JSON array with at least one Explorer URL in it. It's better if there are more than one explorer URLs in this JSON array. Example: `["http://example1.com/tx/","http://example2.com/tx/"]`.
- The URL of Explorer must be pointing to the transactions URL. Check BTC file for an example: [explorers/BTC](explorers/BTC), which has `["https://www.blocktrail.com/BTC/tx/"]`. This explorers URL is used to show in graphical applications the link to the transactions like this [example link](https://www.blocktrail.com/BTC/tx/5268d045196e940ca8ba53b442c38a0f8c159002c912f8427239153dce984cc3/). Make sure this URL ends with `/`.


### 4. Electrum Servers (Optional; Required for listing in Mobile GUIs)
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

### 5. Ethereum info file (Required for ETH/ERC20)

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


### Komodo [electrumX monitoring portal](https://eyelectrumx.herokuapp.com/).

- [Projects repo](https://github.com/dathbezumniy/eyelectrumx)
- [This file](https://github.com/komodoplatform/coins/blob/master/contrib/gui_tickers.json) is monitored by parser in order to automatically rebuild/deploy the portal on any changes to the current integration of coins to the DEX ecosystem.
- It contains json data for parser with up-to-date adex-mob and adex-pro coins integrations as well as all-tickers with available electrum servers that are not yet in our DEX products.
- The maintainer of this file is [dathbezumniy](https://github.com/dathbezumniy).
