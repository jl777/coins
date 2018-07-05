the filenames in each subdirectory needs to match the coin's symbol exactly, that is the unique field that things are indexed by. Also for icons, please use .png files

### About this repository
This repository is the coins database which is accssed by graphical applications like [BarterDEX GUI](https://github.com/KomodoPlatform/BarterDEX). 

When submitting a pull request to add coin to BarterDEX make sure you have completed this checklist:

### 1. Coin info added to `coins` file
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
  "txfee": 100000
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
  "txfee":10000
}

# Example 3
{
  "coin": "REP",
  "name": "augur",
  "fname": "Augur",
  "etomic": "0xE94327D07Fc17907b4DB788E5aDf2ed424adDff6",
  "rpcport": 80
}
```

#### Bitcoin Protocol specific JSON

`"coin"` must be coin ticker.

`"name"` must be coin's name, in all small letters. This is the value which is expected to be default data directory name for that coin. Example if coin's name is `litecoin` then it's expected data directory on Linux is `~/.litecoin/`, on Mac `~/Library/Applications Support/Litecoin/`, on Windows `%AppData%\Litecoin`. Please keep this key's value in small letters only.

`"confpath"` must be ONLY used in case the expected data directory name of the coin/project is different to the `"name"`'s value, as explained in last point. Please refer to Example 2 for better understanding. Make sure to use the exact format for `confpath`. You don't need to change the word `USERHOME`, it remains as is. Make sure you have `/.` after `USERHOME`. And then the expected coin/project's data directory path and it's expected `.conf` file name.

`"fname"` must be coin's full name.

`"rpcport"` must be coin's default RPC port. It is expected that it doesn't conflict with any existing coin in the coins db.

`"pubtype"`, `"p2shtype"`, and `"wiftype"` is the also very specific information about coin's parameters. This is specific to Bitcoin Protocol compatible coins only, and such information can be found in source code of the project. These parameters information can be expected in files like `src/init.cpp`, `src/base58.h`, and `src/chainparamsbase.h` if the project is following the **bitcoin** source code directory/files structure. If the parameters info is unclear then please have these confirmed by that coin/project's developers and make sure it's correct information.

`"txfee"` is a value of default transactions fee, which must be specified in satoshies unit. BarterDEX uses this as the default transaction fee value when makes atomic swaps transactions.


#### Ethereum Protocol specific JSON

Ethereum protocol specific coin/project add request are the most simplest. `"coin"`, `"name"`, and `"fname"` information is same as explained in bitcoin protocol specific json section.

`"rpcport"` must remain default for all ERC20 token/coins. Make sure its only specified as `80`.

`"etomic"` must be the ERC20 token/coin's smart contract address.


### 2. Icon file
- The icon file is required.
- Icon must be a .png format file.
- Dimentions of icon file is 82x82 pixels.
- Icon file name MUST be in **small letters**.
- Icon file location is [icons](icons) directory.


