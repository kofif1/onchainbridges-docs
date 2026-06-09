# Onchain Bridges - Stellar Integration

**Status:** the Soroban stack described here is deployed and live on Stellar testnet, exercised through the public testnet dApp at https://rwa-testnet.onchainbridges.com. It is demo-grade and not yet audited. Every Stellar contract id below is verifiable at `https://stellar.expert/explorer/testnet/contract/<ID>`.

Onchain Bridges is a compliance and interoperability layer for tokenized real-world assets (RWAs). The broader protocol is already live on six EVM testnets and Solana Devnet, all built on Chainlink (CCIP, the Cross-Chain Token standard, the Automated Compliance Engine, the Runtime Environment, and Proof of Reserve). **This document is Stellar-specific:** it describes what we have already built on Soroban, and the Stellar ecosystem building blocks we will integrate with grant funding.

---

## 1. What is already live on Stellar (testnet)

We built a full compliant-RWA stack natively on Soroban to prove the end-to-end lifecycle on Stellar:

- **sMBT** - a compliance-gated RWA token (SEP-41), with allowlist plus pause enforced on every transfer (a Soroban-native equivalent of our EVM compliance engine). Reference asset: "Miami Beach Tower."
- **EVM to Stellar bridge** - a lock-and-mint bridge that moves the real-world-asset token from Polygon (MBT) to Stellar (sMBT), with Chainlink CRE providing DON-verified attestation in both directions. This is a non-CCIP (Category C) lane; it converges to Chainlink CCIP burn-and-mint, with no application change, if and when CCIP-Stellar ships.
- **Native lending** - a Soroban LendingVault ("Polaris") where sMBT is borrowed against in sUSDC.
- **Yield stripping** - a Soroban YieldIssuer mints a tradeable Yield Token (YT) from the RWA's income, and a YTMarket provides a fixed-price secondary market for it. The YT is compliance-gated identically to sMBT.
- **Wallet** - the dApp connects to Stellar and signs Soroban transactions through the **Freighter** wallet (`@stellar/freighter-api`).

### Deployed Soroban contracts (Stellar testnet)

| Contract | Contract ID |
|---|---|
| sMBT (compliance-gated RWA token) | [`CCYOGL2C7OKWDEN7XTIVLS6GFGOUEQQHER36YV5BHLPDCJJM3FIO3TD5`](https://stellar.expert/explorer/testnet/contract/CCYOGL2C7OKWDEN7XTIVLS6GFGOUEQQHER36YV5BHLPDCJJM3FIO3TD5) |
| sUSDC (loan and yield currency) | [`CAS5G444JM4CDTX33ALSMAEJDMKMNKKUIHC3PV7N24KDRENRUVA4DCPO`](https://stellar.expert/explorer/testnet/contract/CAS5G444JM4CDTX33ALSMAEJDMKMNKKUIHC3PV7N24KDRENRUVA4DCPO) |
| LendingVault "Polaris" | [`CB7WBLOFLDFJYKCYFOJYICDW3PUJ66IWIGJMP3P7MDDSXNGY5ON3JINS`](https://stellar.expert/explorer/testnet/contract/CB7WBLOFLDFJYKCYFOJYICDW3PUJ66IWIGJMP3P7MDDSXNGY5ON3JINS) |
| YieldIssuer | [`CDOHKXC63NMVZ6BRK3MYCCEK5LQCUB227YI53EEPYMBGUZRONP6PCAFG`](https://stellar.expert/explorer/testnet/contract/CDOHKXC63NMVZ6BRK3MYCCEK5LQCUB227YI53EEPYMBGUZRONP6PCAFG) |
| YT (compliance-gated yield token) | [`CBTRU54726K5WJV6VMIBFY4WW4SHRJF6DEQB7KKAWF4HAXECAVBISPVC`](https://stellar.expert/explorer/testnet/contract/CBTRU54726K5WJV6VMIBFY4WW4SHRJF6DEQB7KKAWF4HAXECAVBISPVC) |
| YTMarket (fixed-price YT secondary market) | [`CCXKKM7IVCDAYNI2FCN6DILBTDY37ZVUJB6TUWJEF4TS3IBCMY6QDFKD`](https://stellar.expert/explorer/testnet/contract/CCXKKM7IVCDAYNI2FCN6DILBTDY37ZVUJB6TUWJEF4TS3IBCMY6QDFKD) |

### EVM endpoints of the Stellar bridge (Polygon Amoy, chainId 80002, explorer https://amoy.polygonscan.com)

| Contract | Address |
|---|---|
| MBT (the bridged RWA token) | [`0x71A8e443f223cFe59498968758dB49F2D114dCE2`](https://amoy.polygonscan.com/address/0x71A8e443f223cFe59498968758dB49F2D114dCE2) |
| StellarLockVault | [`0xA19DB9d6944ee5181233A3dC02bdB7dffB779C7D`](https://amoy.polygonscan.com/address/0xA19DB9d6944ee5181233A3dC02bdB7dffB779C7D) |
| StellarBridgeOutbox | [`0xbF4158fb88567c2b6a337993Eb0D19CfaC56FB20`](https://amoy.polygonscan.com/address/0xbF4158fb88567c2b6a337993Eb0D19CfaC56FB20) |

These EVM addresses are EIP-55 checksummed; the Stellar contract ids carry their own StrKey checksum.

---

## 2. Existing building-block integration: Freighter

We already integrate one building block from the SCF integration list. **Freighter** (Freighter Connect) is the wallet through which users connect to Stellar and sign every Soroban transaction in our dApp, via `@stellar/freighter-api`. This is live today on the public testnet dApp. It is our anchor integration; the grant-funded work below adds new integrations on top of it.

---

## 3. Integration plan (grant-funded): Blend v2

We built our own Soroban DeFi primitives (the Polaris vault and the YTMarket) to prove the full RWA lifecycle on Stellar. The purpose of this grant is to move the lending side of that lifecycle onto a **Stellar-native building block: Blend v2.**

Plan: list sMBT as eligible collateral in a Blend v2 lending pool (or stand up a dedicated pool), so RWA holders borrow against compliant real-world-asset collateral using Stellar's leading lending protocol instead of our standalone Polaris vault. Our allowlist compliance gates which wallets can supply or borrow, so the pool stays compliant at the asset level. Most of the requested budget goes to this integration; estimated effort aligns with the list's "1+ month."

This is a deliberately focused, realistic scope: one production-grade integration with the leading Stellar lending protocol, on top of the live Freighter anchor. Other Stellar DeFi building blocks (Soroswap and Aquarius for liquidity and swap routing, DeFindex for yield) are natural later phases once the Blend integration is in production; they are not part of this request.

---

## 4. How it fits together

1. A real-world-asset token issued on Polygon (MBT) bridges to Stellar as sMBT via Chainlink CRE, compliance enforced on arrival.
2. On Stellar, sMBT is a compliance-gated SEP-41 token; every transfer passes an allowlist and pause check.
3. Holders borrow against sMBT through Blend v2 lending pools, and strip and trade the asset's yield, all gated by the same compliance.
4. Users connect and sign through Freighter.

The result for Stellar: compliant real-world assets, and the users and liquidity that follow them, are drawn into the Stellar DeFi ecosystem through native building blocks, with compliance enforced on every transfer, and without Stellar or its DeFi protocols having to build RWA compliance themselves.

---

## 5. Production roadmap on Stellar

- Adopt the **OpenZeppelin Soroban RWA library** (ERC-3643 / T-REX) for production-grade, audited compliance on Soroban.
- Wire **Chainlink Proof of Reserve** and **Chainlink Data Streams** on Stellar (both already live on the network) for reserve attestation and pricing of the RWA token.
- Security audit of the Soroban contracts ahead of mainnet.
- Swap the Category C CRE bridge for **Chainlink CCIP** if and when CCIP-Stellar ships, with no application-level change.
