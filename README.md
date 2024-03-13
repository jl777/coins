## What is the coins repository for?

This repository is the coins database which is used to define parameters for coins compatible with the [Komodo DeFi Framework](https://github.com/KomodoPlatform/komodo-defi-framework/), and listed within the apps below:

<p align="center">
    <a href="https://github.com/KomodoPlatform/komodo-wallet-mobile"><img src="https://user-images.githubusercontent.com/35845239/226103567-6d6872de-b0aa-4b87-9ba6-b692be314861.png" alt="Komodo Wallet Mobile"></a>
    <a href="https://app.atomicdex.io"><img src="https://user-images.githubusercontent.com/35845239/226103583-0c1f1b73-80a0-4123-8a4a-bdc2bccd9594.png" alt="Komodo Wallet Web"></a>
    <a href="https://github.com/KomodoPlatform/komodo-wallet-desktop"><img src="https://user-images.githubusercontent.com/35845239/226103576-a0336fcb-0d8e-47db-bf66-6ec779c35f1c.png" alt="Komodo Wallet Desktop"></a>
</p>

Refer to the [coin listing guide](https://developers.komodoplatform.com/basic-docs/atomicdex/atomicdex-tutorials/listing-a-coin-on-atomicdex.html) on the Komodo Developer Documentation website for details about the information required for a successful listing. **To avoid SSL certificate validation issues, it is highly recommended to use [EFF's Certbot](https://certbot.eff.org/) to generate SSL certificates for ElectrumX servers.**

The status of currently listed [ElectrumX](https://electrumx.readthedocs.io/en/latest/) servers is monitored via a public [API](https://electrum-status.dragonhound.info/api/v1/electrums_status) and [Dashboard](https://stats.kmd.io/atomicdex/electrum_status/). Discord status alerts are available in the [AtomicDEX Electrum Status channel](https://discord.gg/rTkjADfnjt) (please contact smk to register and recieve pings when your servers have an issue).

**Note:** _Where ElectrumX or other infrastructure servers are maintained by third party service providers, contact details for service alerts must be provided. It is also recommended to set up monitoring via [Zabbix](https://www.zabbix.com/) and/or [https://1209k.com/bitcoin-eye/ele.php](https://1209k.com/bitcoin-eye/ele.php)_



### Currently supported coins & protocols

AtomicDEX is a true non-custodial, cross-chain, cross-protocol Decentralized Exchange (DEX), allowing for trades between coins and tokens across many platforms and ecosystems, including:

- [UTXO](https://utxo-alliance.org/) based (e.g. [KMD](https://komodoplatform.com/), [BTC](https://www.bitcoin.com/), [LTC](https://litecoin.com/en/), [DASH](https://www.dash.org/), [DOGE](https://dogecoin.com/) & [DGB](https://digibyte.org/en-us/))
- [Binance Smart Chain](https://www.binance.com/en/blog/ecosystem/introducing-bnb-chain-the-evolution-of-binance-smart-chain-421499824684903436) & BEP20 tokens
- [Fantom](https://fantom.foundation/) & FTM20 tokens
- [Harmony](https://github.com/harmony-one/HRC) & HRC20 tokens
- [Ethereum](https://ethereum.org/en/) & ERC20 tokens
- [KuCoin](https://www.kucoin.com/) & KRC20 tokens
- [Polygon](https://polygon.technology/) & PLG20 tokens
- [Avalanche](https://www.avax.com/) & AVX20 tokens
- [Heco Chain](https://www.hecochain.com/en-us/) & HCO20 tokens
- [Moonriver](https://moonbeam.network/networks/moonriver/) & MVR20 tokens
- [QTUM](https://www.qtum.org/) & QRC20 tokens
- "ZHTLC" coins (e.g. [ARRR](https://pirate.black/) & ZOMBIE)
- [COSMOS](https://cosmos.network/) / [Tendermint](https://tendermint.com/)
- [SmartBCH](https://smartbch.org/) & SLP tokens


### Future coins & protocols

- [Emercoin](https://github.com/KomodoPlatform/komodo-defi-framework/issues/1700)
- [TRON & TRC20 tokens](https://github.com/KomodoPlatform/komodo-defi-framework/issues/1542)
- [TON](https://github.com/KomodoPlatform/komodo-defi-framework/issues/1531)
- [Liquid](https://github.com/KomodoPlatform/komodo-defi-framework/issues/1267)
- [Dash Instasend](https://github.com/KomodoPlatform/komodo-defi-framework/issues/1136)
- [OmniLayer](https://github.com/KomodoPlatform/komodo-defi-framework/issues/1087)
- [Lightning network](https://github.com/KomodoPlatform/komodo-defi-framework/issues/1045)
- [Hedera Hashgraph](https://github.com/KomodoPlatform/komodo-defi-framework/issues/979)
- [XMR](https://github.com/KomodoPlatform/komodo-defi-framework/issues/956)
- [Zano](https://github.com/KomodoPlatform/komodo-defi-framework/issues/942)
- [SysCoin Tokens](https://github.com/KomodoPlatform/komodo-defi-framework/issues/938)
- [ERC721 / ERC1155 NFTs](https://github.com/KomodoPlatform/komodo-defi-framework/issues/900)
- [XTZ](https://github.com/KomodoPlatform/komodo-defi-framework/issues/632)
