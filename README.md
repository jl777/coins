
NOTE: The filenames in each subdirectory needs to match the coin's symbol exactly, that is the unique field that things are indexed by. Also for icons, please use .png files

### About this repository
This repository is the coins database which is accessed by graphical applications like [BarterDEX GUI](https://github.com/KomodoPlatform/BarterDEX). 

When submitting a pull request to add coin to BarterDEX make sure you have completed this checklist:

### 0. The coin must be tested with BarterDEX atomic swaps
When submitting your coin add request please post the 5 transactions URLs produced by successful swap in separate file inside [swaps dir](swaps), [example](swaps/BEER-ETOMIC.md). This means that before submitting the further steps information to this coins database repo, you would have performed an atomic swap, and the further steps explains the expected files/values to be submitted to this database repo.

You can learn about performing an atomic swap from our documentation link https://docs.komodoplatform.com

Or you can contact the team at coinintegration@komodoplatform.com to get help if required.

### 1. Coin info added to `coins` file (Required)
You need the following info in JSON format added to [coins](coins) file:

```shell
# Example 1
{
  "coin": "LTC",
  "name": "litecoin",
  "fname": "Litecoin",
  "rpcport": 9332,
  "pubtype": 48,
  "p2shtype": 5,
  "wiftype": 176,
  "txfee": 100000,
  "mm2": 1
}

# Example 2
{
  "coin":"PEW",
  "name":"brofist",
  "fname": "Brofist",
  "confpath": "USERHOME/.brofistcore/brofist.conf"
  "rpcport":12454,
  "pubtype":55,
  "p2shtype":10,
  "wiftype":198,
  "txfee":10000,
  "mm1": 1
}

# Example 3
{
  "coin": "ZEC",
  "name": "zcash",
  "fname": "Zcash",
  "rpcport": 8232,
  "taddr": 28,
  "pubtype": 184,
  "p2shtype": 189,
  "wiftype": 128,
  "txversion": 4,
  "txfee": 10000,
  "overwintered": 1,
  "mm2": 1
},

# Example 4
{
  "coin": "REP",
  "name": "augur",
  "fname": "Augur",
  "etomic": "0xE94327D07Fc17907b4DB788E5aDf2ed424adDff6",
  "rpcport": 80,
  "mm2": 1
}
```

#### General parameters

`"mm2"` add this param if coin is confirmed working with MM2 (successful swap is made). 

`"required_confirmations"` the number of confirmations MM2 will wait for during the swap. Default value is 1.

#### Bitcoin Protocol specific JSON

`"coin"` must be coin ticker.

`"name"` must be coin's name, in all small letters. This is the value which is expected to be default data directory name for that coin. Example if coin's name is `litecoin` then it's expected data directory on Linux is `~/.litecoin/`, on Mac `~/Library/Applications Support/Litecoin/`, on Windows `%AppData%\Litecoin`. Please keep this key's value in small letters only.

`"confpath"` must be ONLY used in case the expected data directory name of the coin/project is different to the `"name"`'s value, as explained in last point. Please refer to Example 2 for better understanding. Make sure to use the exact format for `confpath`. You don't need to change the word `USERHOME`, it remains as is. Make sure you have `/.` after `USERHOME`. And then the expected coin/project's data directory path and it's expected `.conf` file name.

`"fname"` must be coin's full name.

`"rpcport"` must be coin's default RPC port. It is expected that it doesn't conflict with any existing coin in the coins db.

`"pubtype"`, `"p2shtype"`, and `"wiftype"` is the also very specific information about coin's parameters. This is specific to Bitcoin Protocol compatible coins only, and such information can be found in source code of the project. These parameters information can be expected in files like `src/init.cpp`, `src/base58.h`, and `src/chainparamsbase.h` if the project is following the **bitcoin** source code directory/files structure. If the parameters info is unclear then please have these confirmed by that coin/project's developers and make sure it's correct information.

`"txfee"` is a value of default transactions fee, which must be specified in satoshies unit. BarterDEX uses this as the default transaction fee value when makes atomic swaps transactions.

`"overwintered"` must be `1` if Overwinter upgrade was activated for the coin. Defaults to 1 for KMD and assetchains.


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
- The URL of Explorer must be pointing to the transactions URL. Check BTC file for an example: [explorers/BTC](explorers/BTC), which has `["https://www.blocktrail.com/BTC/tx/"]`. This explorers URL is used to show in graphical applications to link to the transactions like this [example link](https://www.blocktrail.com/BTC/tx/5268d045196e940ca8ba53b442c38a0f8c159002c912f8427239153dce984cc3). Make sure this URL ends with `/`.

### 4. Electrum Servers (Optional)

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

- At least minimum 2 or more Electrum servers information must be provided.
- Protocol can be "SSL" or "TCP".
- Contact information must be provided in case the server admin needs to be contact in urgent cases when required. It can be any contact information out of the examples provided. Or may be add your own service/contact information as suites you.
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
