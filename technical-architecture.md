# Onchain Bridges - Technical Architecture

**Status:** pre-mainnet. Every contract below is deployed and live on a public testnet and is independently verifiable on the linked block explorer. The system is demo-grade and not yet audited; a formal audit precedes mainnet.

Onchain Bridges is the compliance and interoperability layer for tokenized real-world assets (RWAs). It is built on Chainlink (CCIP, the Cross-Chain Token standard, the Automated Compliance Engine, the Runtime Environment, and Proof of Reserve), so we add the RWA application layer rather than operating our own bridge or validators. The full system, including the Stellar stack, is usable today through the public testnet dApp at https://rwa-testnet.onchainbridges.com.

---

## 1. System layers

1. **Asset layer.** An RWA is issued once as a single canonical token (the reference asset is MBT, "Miami Beach Tower"). The same token exists natively on every supported chain.
2. **Compliance layer.** Every mint, transfer, and cross-chain arrival is gated by a policy check (allowlist, jurisdiction, pause). A regulated asset can never land in an ineligible wallet.
3. **Transport layer.** Chainlink CCIP carries the token between CCIP-supported chains by burn-and-mint, with no wrapped copies. Chainlink CRE extends the same compliance-gated flow to non-CCIP chains.
4. **DeFi layer.** Yield stripping (principal plus a tradeable Yield Token), a cross-chain lending marketplace, and a YT secondary market make the asset productive.
5. **Account-abstraction layer.** A paymaster lets users pay fees and gas in a single token (TLPT).

## 2. Compliance-gated transfer flow

1. The user initiates a transfer.
2. Identity is referenced through the chain's allowlist (PolicyEngine plus AllowPolicy on EVM; the equivalent native primitive on non-EVM chains).
3. On a cross-chain transfer the token is burned on the source chain (or locked, on the lock-and-mint lanes).
4. A cross-chain message is delivered by Chainlink CCIP, or by a Chainlink CRE DON-signed report on non-CCIP lanes.
5. The destination executes the mint only if the destination compliance check passes. A non-allowlisted recipient causes the entire transfer to revert.

## 3. Compliance model (Chainlink ACE)

On every EVM chain the token routes each transfer through a `PolicyEngine` with two policies attached: `AllowPolicy` (allowlist enforcement) and `PausePolicy` (emergency halt). Policies are external and upgradeable, so compliance rules evolve without redeploying or migrating the token. On chains where ACE is not available, the same allowlist and pause semantics are inlined into the token contract (Sonic `WrappedMBT v2`) or implemented in the chain's native primitives (a Soroban contract on Stellar, an SPL Token-2022 transfer hook on Solana).

## 4. Cross-chain routing

| Tier | Used when | Provider |
|---|---|---|
| 1 | Both chains are CCIP-supported | Chainlink CCIP, burn-and-mint via the Cross-Chain Token standard |
| 2 | A chain is not CCIP-supported | Chainlink CRE, DON-signed reports verifying source-chain events |
| 3 | Long-tail chains beyond CCIP and CRE | Onboarded in-house or via additional providers under evaluation |

We do not operate validators or relayers. The highest-risk layer in the industry is delegated to Chainlink, and we add the application layer on top.

## 5. Proof of Reserve

The RWA token's mint path carries a Chainlink Proof of Reserve hook: a mint reverts if the reserve feed is stale or reports insufficient backing. The hook is wired into the token contract today; the live per-issuer feed is configured at issuer onboarding before mainnet.

## 6. DeFi layer

- **Yield stripping.** A `YieldIssuer` opens periods and mints a Yield Token (YT) proportional to each holder's balance. The YT is compliance-gated identically to the underlying asset.
- **YT secondary market.** A `YTMarket` is a fixed-price market where holders list and buy YT, so the income stream trades independently of the principal.
- **Lending marketplace.** Per-chain LendingVaults accept the RWA token as collateral and compete on terms; the best deal is surfaced in one interface.

## 7. Account abstraction

An ERC-4337 paymaster (TLPTPaymaster) lets users pay protocol fees and gas in TLPT. It is deployed on testnet across several chains. It is not yet enabled as a user-facing surface; the single-fee abstraction is being completed before it is exposed.

---

## 8. Deployed contracts (testnet)

All addresses are EIP-55 checksummed and were verified with `cast to-checksum`. Each links to the chain's public block explorer.

### Ethereum Sepolia (chainId 11155111) - explorer: https://sepolia.etherscan.io

| Contract | Address |
|---|---|
| MBT (RWA token) | [`0x044951AB857C7e23b5570D4ca11466ACACF861A8`](https://sepolia.etherscan.io/address/0x044951AB857C7e23b5570D4ca11466ACACF861A8) |
| BurnMintTokenPool | [`0x53d88a3Fe9480767bE210CbC2e2b3E14145D087d`](https://sepolia.etherscan.io/address/0x53d88a3Fe9480767bE210CbC2e2b3E14145D087d) |
| PolicyEngine | [`0xd4b9F980f09f0871C753a7d558B5c500DA1617a3`](https://sepolia.etherscan.io/address/0xd4b9F980f09f0871C753a7d558B5c500DA1617a3) |
| AllowPolicy | [`0x7858b6e699c381583A8A820F52AF051197B3DCD1`](https://sepolia.etherscan.io/address/0x7858b6e699c381583A8A820F52AF051197B3DCD1) |
| PausePolicy | [`0x2038964Aea77Aa4A7cfB6a8A769e83FD119e634A`](https://sepolia.etherscan.io/address/0x2038964Aea77Aa4A7cfB6a8A769e83FD119e634A) |
| Proof of Reserve feed | [`0xf88882929AA3ABcDf6A9B976AA33B4158C918c1C`](https://sepolia.etherscan.io/address/0xf88882929AA3ABcDf6A9B976AA33B4158C918c1C) |
| YieldIssuer | [`0x34b8822b44ff287a2c7C6Fa8Fad60B0DC27AB841`](https://sepolia.etherscan.io/address/0x34b8822b44ff287a2c7C6Fa8Fad60B0DC27AB841) |
| YT-MBT | [`0x7f939bc5e0db02910a461EE49127df881D042299`](https://sepolia.etherscan.io/address/0x7f939bc5e0db02910a461EE49127df881D042299) |
| YTMarket | [`0xa25cC783b6CBb51CBCA57dC012315ef38212c94E`](https://sepolia.etherscan.io/address/0xa25cC783b6CBb51CBCA57dC012315ef38212c94E) |
| TLPT (fee token) | [`0x1ceaaE761C87278acfbE33c89eC523B46FAbCcF3`](https://sepolia.etherscan.io/address/0x1ceaaE761C87278acfbE33c89eC523B46FAbCcF3) |
| TLPTPaymaster v2.1 | [`0xc4F407562b446f024fF9bDdDB390D8a499552c82`](https://sepolia.etherscan.io/address/0xc4F407562b446f024fF9bDdDB390D8a499552c82) |

### Polygon Amoy (chainId 80002) - explorer: https://amoy.polygonscan.com

| Contract | Address |
|---|---|
| MBT (RWA token) | [`0x71A8e443f223cFe59498968758dB49F2D114dCE2`](https://amoy.polygonscan.com/address/0x71A8e443f223cFe59498968758dB49F2D114dCE2) |
| BurnMintTokenPool | [`0x48dB3f62B6c7328Fb742B4799654136794dBE2B4`](https://amoy.polygonscan.com/address/0x48dB3f62B6c7328Fb742B4799654136794dBE2B4) |
| PolicyEngine | [`0xfefA774dB9A52c72EC8f0621046836CbA63d2BA6`](https://amoy.polygonscan.com/address/0xfefA774dB9A52c72EC8f0621046836CbA63d2BA6) |
| AllowPolicy | [`0x5fe9d900945b60B3BEcEDe4382BEd2653EC99D40`](https://amoy.polygonscan.com/address/0x5fe9d900945b60B3BEcEDe4382BEd2653EC99D40) |
| PausePolicy | [`0x8c57Abe7Cf1330346EB760EDaEE380A66D3f42f7`](https://amoy.polygonscan.com/address/0x8c57Abe7Cf1330346EB760EDaEE380A66D3f42f7) |
| YieldIssuer | [`0x62BD210F9e7B4889066Bd7bc360557c666af44F5`](https://amoy.polygonscan.com/address/0x62BD210F9e7B4889066Bd7bc360557c666af44F5) |
| YT-MBT | [`0xC4dE838dF59AEB7a9Ad099A34EE6F3E1B19D1aeC`](https://amoy.polygonscan.com/address/0xC4dE838dF59AEB7a9Ad099A34EE6F3E1B19D1aeC) |
| YTMarket | [`0xa701147b7C1a511790BE503675Df1F8B09caBAa9`](https://amoy.polygonscan.com/address/0xa701147b7C1a511790BE503675Df1F8B09caBAa9) |
| StellarLockVault (Stellar bridge endpoint) | [`0xA19DB9d6944ee5181233A3dC02bdB7dffB779C7D`](https://amoy.polygonscan.com/address/0xA19DB9d6944ee5181233A3dC02bdB7dffB779C7D) |
| StellarBridgeOutbox (Stellar bridge endpoint) | [`0xbF4158fb88567c2b6a337993Eb0D19CfaC56FB20`](https://amoy.polygonscan.com/address/0xbF4158fb88567c2b6a337993Eb0D19CfaC56FB20) |

### Plume Testnet (chainId 98867) - explorer: https://testnet-explorer.plume.org

| Contract | Address |
|---|---|
| MBT (RWA token) | [`0x43CC10a0bbEb70d8EFCb45714e0e0F4C49500c75`](https://testnet-explorer.plume.org/address/0x43CC10a0bbEb70d8EFCb45714e0e0F4C49500c75) |
| PolicyEngine | [`0x045A3c91E4742aAeb9b3E0E5d87A0b94B801c6D3`](https://testnet-explorer.plume.org/address/0x045A3c91E4742aAeb9b3E0E5d87A0b94B801c6D3) |
| AllowPolicy | [`0x2aedDb48a3b6028244ed31C0fdDEB2B72Fce3bE1`](https://testnet-explorer.plume.org/address/0x2aedDb48a3b6028244ed31C0fdDEB2B72Fce3bE1) |
| PausePolicy | [`0x5D273AAE0547FD33c0C5247487a160cd26f38FE4`](https://testnet-explorer.plume.org/address/0x5D273AAE0547FD33c0C5247487a160cd26f38FE4) |
| YieldIssuer | [`0xBe0107334394e9b8ccBE18e9D39e3c3C1f302B00`](https://testnet-explorer.plume.org/address/0xBe0107334394e9b8ccBE18e9D39e3c3C1f302B00) |
| YT-MBT | [`0x6eB381e96d39a2393652deD532f304D297602EAe`](https://testnet-explorer.plume.org/address/0x6eB381e96d39a2393652deD532f304D297602EAe) |
| YTMarket | [`0x6c1F0bF40De396292310440ABE8f89996beA0F3E`](https://testnet-explorer.plume.org/address/0x6c1F0bF40De396292310440ABE8f89996beA0F3E) |

### Astar Shibuya (chainId 81) - explorer: https://shibuya.blockscout.com

| Contract | Address |
|---|---|
| MBT (RWA token) | [`0xF08a207bb7D0198356ED4Fffd555Ee7129E2b8f5`](https://shibuya.blockscout.com/address/0xF08a207bb7D0198356ED4Fffd555Ee7129E2b8f5) |
| BurnMintTokenPool | [`0x1febE4cf83C444b012dcEE7bbcE145fC66c1B06D`](https://shibuya.blockscout.com/address/0x1febE4cf83C444b012dcEE7bbcE145fC66c1B06D) |
| PolicyEngine | [`0xb48b0Ed177647723cE6E4C306D62B1037Bc44967`](https://shibuya.blockscout.com/address/0xb48b0Ed177647723cE6E4C306D62B1037Bc44967) |
| ComplianceCheck (combined Allow + Pause) | [`0xce8C237c6b8bF91df589eA740d4d65Cbb75F7DDd`](https://shibuya.blockscout.com/address/0xce8C237c6b8bF91df589eA740d4d65Cbb75F7DDd) |

### Sonic Testnet (chainId 14601, non-CCIP, CRE-bridged) - explorer: https://testnet.sonicscan.org

| Contract | Address |
|---|---|
| WrappedMBT v2 (compliance-gated) | [`0x670c3a58435cc13e9edA059F4093F31CedEEF7F3`](https://testnet.sonicscan.org/address/0x670c3a58435cc13e9edA059F4093F31CedEEF7F3) |
| CREBridgeConsumer v2 | [`0xA56efb5A85A2C9c2e07478Ce257CEdEcEE9cA7f6`](https://testnet.sonicscan.org/address/0xA56efb5A85A2C9c2e07478Ce257CEdEcEE9cA7f6) |
| Nova Finance LendingVault | [`0x49f1aa7C252183E79D4944c54698a335Ed65C150`](https://testnet.sonicscan.org/address/0x49f1aa7C252183E79D4944c54698a335Ed65C150) |
| YieldIssuer | [`0xe43355DFBfaa167B76591432c1d033a454B87AD3`](https://testnet.sonicscan.org/address/0xe43355DFBfaa167B76591432c1d033a454B87AD3) |
| YT-MBT | [`0x73362F49F5dB3f1253D73a4f017f2324b6e113e0`](https://testnet.sonicscan.org/address/0x73362F49F5dB3f1253D73a4f017f2324b6e113e0) |
| YTMarket | [`0x3c4070794aa047decCdb42bD9BbE37a4310fa9b9`](https://testnet.sonicscan.org/address/0x3c4070794aa047decCdb42bD9BbE37a4310fa9b9) |

### Solana Devnet (non-EVM, compliance enforced via SPL Token-2022 transfer hook) - explorer: https://explorer.solana.com (cluster=devnet)

| Program / account | Address |
|---|---|
| mbt-allowlist-hook program | [`7AV99KFhxpn1XpkkRAaW5peSZxqrDWFTA3JrYjDXGqrs`](https://explorer.solana.com/address/7AV99KFhxpn1XpkkRAaW5peSZxqrDWFTA3JrYjDXGqrs?cluster=devnet) |
| Wrapped-MBT mint (SPL Token-2022) | [`ENndzpMJtnMigJpvJFiB2JrdZH5wMvtcmYFoTM7Tadiz`](https://explorer.solana.com/address/ENndzpMJtnMigJpvJFiB2JrdZH5wMvtcmYFoTM7Tadiz?cluster=devnet) |
| mbt-bridge-delivery program | [`AcapDYPqWuZP64E3dA2mtFf8CG9GLbvJd1fQHhTym45Y`](https://explorer.solana.com/address/AcapDYPqWuZP64E3dA2mtFf8CG9GLbvJd1fQHhTym45Y?cluster=devnet) |

### Stellar Testnet (Soroban, non-EVM) - explorer: https://stellar.expert/explorer/testnet

A full compliant RWA stack runs natively on Soroban: a compliance-gated token, a lock-and-mint bridge from Polygon Amoy with Chainlink CRE DON-verified attestation, native lending, yield stripping, and a YT secondary market. Compliance (allowlist plus pause) is enforced in the Soroban token on every transfer. This stack is live on the public testnet dApp at https://rwa-testnet.onchainbridges.com.

| Contract | Address |
|---|---|
| sMBT (compliance-gated RWA token) | [`CCYOGL2C7OKWDEN7XTIVLS6GFGOUEQQHER36YV5BHLPDCJJM3FIO3TD5`](https://stellar.expert/explorer/testnet/contract/CCYOGL2C7OKWDEN7XTIVLS6GFGOUEQQHER36YV5BHLPDCJJM3FIO3TD5) |
| sUSDC (loan and yield currency) | [`CAS5G444JM4CDTX33ALSMAEJDMKMNKKUIHC3PV7N24KDRENRUVA4DCPO`](https://stellar.expert/explorer/testnet/contract/CAS5G444JM4CDTX33ALSMAEJDMKMNKKUIHC3PV7N24KDRENRUVA4DCPO) |
| LendingVault "Polaris" (borrow sUSDC against sMBT) | [`CB7WBLOFLDFJYKCYFOJYICDW3PUJ66IWIGJMP3P7MDDSXNGY5ON3JINS`](https://stellar.expert/explorer/testnet/contract/CB7WBLOFLDFJYKCYFOJYICDW3PUJ66IWIGJMP3P7MDDSXNGY5ON3JINS) |
| YieldIssuer | [`CDOHKXC63NMVZ6BRK3MYCCEK5LQCUB227YI53EEPYMBGUZRONP6PCAFG`](https://stellar.expert/explorer/testnet/contract/CDOHKXC63NMVZ6BRK3MYCCEK5LQCUB227YI53EEPYMBGUZRONP6PCAFG) |
| YT (compliance-gated yield token) | [`CBTRU54726K5WJV6VMIBFY4WW4SHRJF6DEQB7KKAWF4HAXECAVBISPVC`](https://stellar.expert/explorer/testnet/contract/CBTRU54726K5WJV6VMIBFY4WW4SHRJF6DEQB7KKAWF4HAXECAVBISPVC) |
| YTMarket (fixed-price YT secondary market) | [`CCXKKM7IVCDAYNI2FCN6DILBTDY37ZVUJB6TUWJEF4TS3IBCMY6QDFKD`](https://stellar.expert/explorer/testnet/contract/CCXKKM7IVCDAYNI2FCN6DILBTDY37ZVUJB6TUWJEF4TS3IBCMY6QDFKD) |

The EVM endpoints of the Stellar bridge are the StellarLockVault and StellarBridgeOutbox on Polygon Amoy, listed in the Amoy table above. The bridge is non-CCIP (lock-and-mint via Chainlink CRE plus keepers) and converges to CCIP burn-and-mint with no application change if Chainlink adds Stellar to CCIP.

---

## 9. Planned additions and improvements

- **Stellar mainnet readiness:** harden and audit the Soroban stack; adopt the OpenZeppelin Soroban RWA library (ERC-3643 / T-REX); wire in Chainlink Proof of Reserve and Data Streams, which are already live on Stellar; swap the CRE bridge for CCIP if and when Chainlink ships CCIP-Stellar.
- **Account abstraction Phase 2:** complete the single-fee abstraction (paymaster LINK reserve plus TLPT-to-LINK swap) and expose it in the dApp.
- **Portable identity:** a reusable KYC credential (DID / Verifiable Credentials) so one onboarding works across chains.
- **Per-issuer Proof of Reserve:** live reserve feeds configured per real issuer at mainnet onboarding.
