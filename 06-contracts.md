---
title: "Contract Reference"
---

# 6. Contract Reference

[← Back to index](README.md)

Live testnet addresses across every supported chain. Authoritative source: `webapp/src/config/chains.ts` (this document is a snapshot).

> Last updated and verified: 2026-06-05. §6.1-6.6 (EVM chains + yield) verified against the webapp config files, all addresses match. §6.8 (Solana Devnet): Phase B is complete; C-lite trust-minimized recipient-claim path verified end-to-end on Devnet (2026-05-20), exposed in the dApp as of 2026-06-05 via the V1 C-lite message shape, with the V2 atomic path preserved in code (svmCcip.ts `buildBridgeMessageV2`) for when Chainlink unblocks the offramp heap-OOM. §6.10 (Account Abstraction contracts) added 2026-05-17.
>
> This document is the canonical contract registry. Per CLAUDE.md invariant 5, any contract added, removed, redeployed, or deprecated on any chain is reflected here in the same commit.

## 6.1 Sepolia (chainId 11155111)

| Contract | Address |
|---|---|
| **MBT (RWA token)** | `0x044951AB857C7e23b5570D4ca11466ACACF861A8` |
| **BurnMintTokenPool** | `0x53d88a3Fe9480767bE210CbC2e2b3E14145D087d` |
| **PolicyEngine** | `0xd4b9F980f09f0871C753a7d558B5c500DA1617a3` |
| **AllowPolicy** | `0x7858b6e699c381583A8A820F52AF051197B3DCD1` |
| **PausePolicy** | `0x2038964Aea77Aa4A7cfB6a8A769e83FD119e634A` |
| **PoR Reserve Feed** | `0xf88882929AA3ABcDf6A9B976AA33B4158C918c1C` |

CCIP Router: `0x0BF3dE8c5D3e8A2B34D2BEeB17ABfCeBaf363A59` (Chainlink-hosted)
LINK token: `0x779877A7B0D9E8603169DdbD7836e478b4624789`

## 6.2 Polygon Amoy (chainId 80002)

| Contract | Address |
|---|---|
| **MBT (RWA token)** | `0x71A8e443f223cFe59498968758dB49F2D114dCE2` |
| **BurnMintTokenPool** | `0x48dB3f62B6c7328Fb742B4799654136794dBE2B4` |
| **PolicyEngine** | `0xfefA774dB9A52c72EC8f0621046836CbA63d2BA6` |
| **AllowPolicy** | `0x5fe9d900945b60B3BEcEDe4382BEd2653EC99D40` |
| **PausePolicy** | `0x8c57Abe7Cf1330346EB760EDaEE380A66D3f42f7` |
| **LockVault** (CRE source for Sonic) | `0x5D273AAE0547FD33c0C5247487a160cd26f38FE4` |
| **MockUSDC** | `0xce8c237c6b8bf91df589ea740d4d65cbb75f7ddd` |

CCIP Router: `0x9C32fCB86BF0f4a1A8921a9Fe46de3198bb884B2`
LINK token: `0x0Fd9e8d3aF1aaee056EB9e802c3A762a667b1904`

## 6.3 Plume Testnet (chainId 98867)

| Contract | Address |
|---|---|
| **MBT (RWA token)** | `0x43cc10a0bbeb70d8efcb45714e0e0f4c49500c75` |
| **BurnMintTokenPool** | `0x8c57abe7cf1330346eb760edaee380a66d3f42f7` |
| **PolicyEngine** | `0x045a3c91e4742aaeb9b3e0e5d87a0b94b801c6d3` |
| **AllowPolicy** | `0x2aedDb48a3b6028244ed31C0fdDEB2B72Fce3bE1` |
| **PausePolicy** | `0x5d273aae0547fd33c0c5247487a160cd26f38fe4` |

CCIP Router: `0x5e5Fd4720E1CE826138D043aF578D69f48af502F`
LINK token: `0xB97e3665AEAF96BDD6b300B2e0C93C662104A068`

> Plume's inbound CCIP from Sepolia is live as of 2026-05-14 after Chainlink raised the per-token gas overhead. End-to-end verification: deployer received 10 MBT on Plume via tx `0x6787e45ffbcf6e3dc2c872e015c4695f02f861a3243caecce3cf8c7f24b6cfe7` and `0x6d07538f367658d1b9674b2c4eb19884b20d2fca92976d95d4c93d1704fd1e1b`.

## 6.4 Astar Shibuya (chainId 81) - dApp lane currently hidden

| Contract | Address |
|---|---|
| **MBT (RWA token)** | `0xf08a207bb7d0198356ed4fffd555ee7129e2b8f5` |
| **BurnMintTokenPool** | `0x1febe4cf83c444b012dcee7bbce145fc66c1b06d` |
| **PolicyEngine** | `0xb48b0ed177647723ce6e4c306d62b1037bc44967` |
| **ComplianceCheck** (combined Allow + Pause) | `0xce8c237c6b8bf91df589ea740d4d65cbb75f7ddd` |

CCIP Router: `0x22aE550d87eBf775E0c1fDc8881121c8A51F5903`
LINK token: `0xe74037112db8807B3B4B3895F5790e5bc1866a29`

> Shibuya contracts remain deployed but the dApp lane is hidden as of 2026-05-14. Sepolia <-> Shibuya CCIP lane shows zero OffRamp activity over a 33h window (v1.5 OffRamp `0x4E773089d04E2CA777BFbC6f15150A3e542ABC7a` and v1.2 OffRamp `0xF389104dFaD66cED6B77b879FF76b572a8cC3590` both quiet). Awaiting Chainlink confirmation of lane status (active / decommissioned / migrating to v1.6).

## 6.5 Sonic Testnet (chainId 14601) — non-CCIP, CRE-bridged

| Contract | Address |
|---|---|
| **WrappedMBT v2** (compliance-gated) | `0x670c3a58435cc13e9edA059F4093F31CedEEF7F3` |
| **CREBridgeConsumer v2** | `0xA56efb5A85A2C9c2e07478Ce257CEdEcEE9cA7f6` |
| **KeystoneForwarder** (Chainlink-hosted) | `0x98B8335d29Aca40840Ed8426dA1A0aAa8677d8D1` |
| **Nova Finance LendingVault v2** (wMBT v2 collateral) | `0x49f1aa7C252183E79D4944c54698a335Ed65C150` |
| **TestUSDC** (Nova vault liquidity + yield currency) | `0x43CC10a0bbEb70d8EFCb45714e0e0F4C49500c75` |
| **YieldIssuer** | `0x905142640A63B582E954C14e7Ed98a49E165D9Ef` |
| **YT-MBT token** | `0x02670162368541ae0098C5C6b76B60Ee0DD749Cf` |
| **YTMarket** | `0xFf586b23d45B4BE1677f19c1589A60321631069e` |

WrappedMBT v2 has built-in allowlist + pause (no separate AllowPolicy contract). Admin functions: `allowAddress`, `disallowAddress`, `allowAddresses`, `setPaused`, `setMinter`, `addressAllowed(view)`.

> v1 wMBT at `0x9139FbB66e770EB3baBCbC7fD59Ef690bCfA7784` is **deprecated** — pre-ACE compliance migration. 14 wMBT v1 tokens are stranded in test wallets; the dApp no longer reads from this contract.

## 6.6 Yield-stripping deployments (per chain)

YieldIssuer + YT token + YTMarket addresses for each chain that runs the yield product:

### Sepolia
- YieldIssuer: `0xF18ff2C7CB1B699d92EfDfc91c1D963BC8E97B7D` (2026-06-16 per-period-snapshot redeploy, PR #36)
- YT-MBT token: `0x206b4FFF5e128e9257dF762cd4872c57e161765A` (compliance-gated; `allowPolicy()` returns the Sepolia AllowPolicy; per-period balance snapshot)
- YTMarket: `0xa8d5924B4Ee9580E8Cb53b3a6cD22E27Df77AD50` (2026-06-16 redeploy; allowlisted on Sepolia AllowPolicy)
- TestUSDC: `0x8bd2a0a9f90dc40a3a420c84553d40dd688035df`

> Superseded by the 2026-06-16 snapshot redeploy (do not import): the 2026-06-03 compliance-fix Sepolia stack (YieldIssuer `0x34b8822b...`, YT `0x7f939bc5...`, YTMarket `0xa25cC783...`); and before it, the pre-2026-06-03-fix stack (plain ERC-20 YT, non-KYC wallets could buy through YTMarket; see `docs/design/yt-mbt-compliance-fix.md`): YieldIssuer `0x207bba4c...`, YT `0x4142f0D3...`, YTMarket `0xec6ed8b7...`.

> Old/deprecated Sepolia yield deployments (built on an orphaned MockUSDC, no longer in use): YieldIssuer `0x6c1f0bf4…`, YT `0xeC7F0BbD…`, YTMarket `0x65fb4431…`. Do not import these.

### Amoy
- YieldIssuer: `0xfd47b73338331fa760D7C96E21A096Dd418ce94D` (2026-06-16 per-period-snapshot redeploy, PR #36)
- YT-MBT token: `0x4390c38a4DE1e7B9eBa1b4C9501986260Fb890E6` (compliance-gated; `allowPolicy()` returns the Amoy AllowPolicy; per-period balance snapshot)
- YTMarket: `0xEecD98365C8E47a0E8cEadd89eC464663272ECF1` (2026-06-16 redeploy; allowlisted on Amoy AllowPolicy)
- USDC: `0xce8c237c6b8bf91df589ea740d4d65cbb75f7ddd`

> Superseded by the 2026-06-16 snapshot redeploy (do not import): the 2026-06-04 compliance-fix Amoy stack (YieldIssuer `0x62BD210F...`, YT `0xC4dE838d...`, YTMarket `0xa701147b...`); and before it, the pre-2026-06-03-fix stack (plain ERC-20 YT): YieldIssuer `0x0fb97310...`, YT `0x42495e16...`, YTMarket `0xf08a2070...`.

### Plume
- YieldIssuer: `0xc8567316b25e74b5196BcD1F27A4CE1733712F19` (2026-06-16 per-period-snapshot redeploy, PR #36)
- YT-MBT token: `0x25bFB440D43AA62E3C0904428497f8ed10460a62` (compliance-gated; `allowPolicy()` returns the Plume AllowPolicy; per-period balance snapshot)
- YTMarket: `0xa9ACC61C20ebE4e49059740641b8d9BCf732295D` (2026-06-16 redeploy; allowlisted on Plume AllowPolicy)
- USDC: `0x22e34a3a9c54a736f9ffdf15a3c4cdc886ff0da6`

> Superseded by the 2026-06-16 snapshot redeploy (do not import): the 2026-06-04 compliance-fix Plume stack (YieldIssuer `0xBe010733...`, YT `0x6eB381e9...`, YTMarket `0x6c1F0bF4...`); and before it, the pre-2026-06-03-fix stack (plain ERC-20 YT): YieldIssuer `0xf3186574...`, YT `0x470A4f73...`, YTMarket `0xfefa774d...`.

### Sonic Testnet (deployed 2026-05-06 — first non-CCIP chain with full yield product)
- YieldIssuer: `0x905142640A63B582E954C14e7Ed98a49E165D9Ef` (2026-06-16 per-period-snapshot redeploy, PR #36)
- YT-MBT token: `0x02670162368541ae0098C5C6b76B60Ee0DD749Cf` (compliance-gated; `allowPolicy()` returns wMBT v2, which inlines the allowlist; per-period balance snapshot)
- YTMarket: `0xFf586b23d45B4BE1677f19c1589A60321631069e` (2026-06-16 redeploy; allowlisted on wMBT v2 via `allowAddress`)

> Superseded by the 2026-06-16 snapshot redeploy (do not import): the 2026-06-04 compliance-fix Sonic stack (YieldIssuer `0xe43355DF...`, YT `0x73362F49...`, YTMarket `0x3c407079...`); and before it, the pre-2026-06-03-fix stack (plain ERC-20 YT): YieldIssuer `0xc38e9d12...`, YT `0x0954Ca93...`, YTMarket `0x0ae06a1a...`.
- RWA token (wMBT v2 — compliance-gated): `0x670c3a58435cc13e9edA059F4093F31CedEEF7F3`
- TestUSDC: `0x43CC10a0bbEb70d8EFCb45714e0e0F4C49500c75`

## 6.7 Lending vaults

| Chain | Provider | LendingVault | USDC |
|---|---|---|---|
| Sepolia | Meridian Lending | (see `webapp/src/config/defi.ts`) | (see same file) |
| Amoy | Atlas Capital | | |
| Sonic | Nova Finance | | |
| Plume | Plumage Finance | | |

Authoritative source: `webapp/src/config/defi.ts`.

## 6.8 Solana Devnet — non-EVM (Category B), Phase A + Phase B

| Contract | Address |
|---|---|
| **mbt-allowlist-hook program** | `7AV99KFhxpn1XpkkRAaW5peSZxqrDWFTA3JrYjDXGqrs` |
| **Wrapped-MBT mint** (SPL Token-2022) | `ENndzpMJtnMigJpvJFiB2JrdZH5wMvtcmYFoTM7Tadiz` |
| **Allowlist config PDA** | `75BvNn9FXbJcQts7piRRChcsDgA2sxBSC4np5jzhrL1p` |
| **ExtraAccountMetaList PDA** | `3C39RWz9R8wnanjVtqL1oXfMBxhd4625NEPuyjEYCiyp` |
| **mbt-bridge-delivery program** | `AcapDYPqWuZP64E3dA2mtFf8CG9GLbvJd1fQHhTym45Y` |
| **Escrow config PDA** | `BoRq3UKuQznsT4VBCSEeg7CcBhoXg8MKGnxatrvhZxz` |
| **Escrow authority PDA** | `3ZsLonSFLnJ54JhJ1T6kGVBaoPU72S2p8eP1FnGnyw6R` |
| **Escrow token account** (holds inbound wrapped-MBT) | `C4yjgA7v594fBBXsu3LtHxxvGcET9vmSf3xNDW74hgXM` |

**Chainlink CCIP CCT pool** (wrapped-MBT registered as a Cross-Chain Token):

| Contract | Address |
|---|---|
| **CCIP BurnMint token-pool program** (canonical, Chainlink-operated) | `41FGToCmdaWa1dgZLKFAjvmx6e6AjVTX7SVRibvsMGVB` |
| **CCIP Router** (Devnet, Chainlink-operated) | `Ccip842gzYHhvdDkSyi2YVCoAWPbYJoApMFzSxQroE9C` |
| **Pool config / state PDA** (wrapped-MBT) | `A5gue4GMvcuuFuHMqkuKZDpca8WMaPnTF9GioM3crdfh` |
| **Pool signer PDA** | `9DZfW6BvouJY6cbPRL8v9VF5pubySYeBUbTR9QSHN6Ky` |
| **Pool token account** | `Z1Hsea5QmUBSx71241SZqKcFHV7Xt42kyZkTvbUMzZF` |
| **Address Lookup Table** (pool ALT) | `RQzEV89dLtYMjmPzXW6k8FBcYKXg4FPhcCWZi2dYhwd` |
| **Sepolia-lane chain-config PDA** | `7zHNGtk9uAhWDQ9GT2kCfprkvSSbNMi6cLUh6K6GHLfN` |

`mbt-allowlist-hook` is the Solana-native equivalent of the EVM ACE AllowPolicy: an SPL Token-2022 transfer-hook that rejects a wrapped-MBT transfer unless the recipient is allowlisted. Upgrade + allowlist authority: the Devnet deployer `Bx4vCP6REyxF9ESme9qvm6Vj8nXCzKbPdi39udrHsLAe`.

`mbt-bridge-delivery` (Phase B) is the inbound-bridge compliance gate. SPL Token-2022 transfer hooks do not fire on `mint_to`, so a stock Chainlink CCIP burn-and-mint pool minting straight to a recipient would bypass the allowlist. Instead the pool mints inbound wrapped MBT into the program-owned escrow token account above, and the program's `deliver` step releases it to the final recipient through a real Token-2022 transfer, which triggers `mbt-allowlist-hook` and enforces the allowlist on inbound bridge deliveries. Escrow admin + keeper: the Devnet deployer `Bx4vCP6REyxF9ESme9qvm6Vj8nXCzKbPdi39udrHsLAe`.

The wrapped-MBT mint is registered as a CCIP Cross-Chain Token, and the Sepolia ↔ Solana Devnet lane is wired on both sides. Solana side: the BurnMint pool config is initialized in Chainlink's canonical Devnet pool program, the Sepolia remote chain is configured (chain-config PDA above, Sepolia pool + token registered, rate limits disabled), the pool ALT is registered with the Token Admin Registry, and the Devnet deployer is the registry administrator. EVM side: the Sepolia MBT pool `0x53d88a3Fe9480767bE210CbC2e2b3E14145D087d` has Solana Devnet added as a remote chain (`applyChainUpdates`, tx `0xa01d4eaa4963cdea3a897c3762408ec392ef04419654b3feca437095eaa2f701`), registering the Solana pool state PDA as the remote pool and the wrapped-MBT mint as the remote token. The wrapped-MBT mint authority has been transferred to the pool signer PDA `9DZfW6BvouJY6cbPRL8v9VF5pubySYeBUbTR9QSHN6Ky`, so inbound CCIP deliveries mint wrapped MBT and nothing else can.

**Phase B is complete and verified end-to-end** (2026-05-19): 10 MBT bridged Sepolia → Solana Devnet (CCIP message `0x43ef48117a07b43dd1e4773f509af54971b7a55d427565c61abd23f985897eea`), minted into the escrow, then `deliver` released 6 to an allowlisted recipient (succeeded, through the transfer hook) and a delivery to a non-allowlisted recipient was rejected by the hook (`NotAllowlisted`), leaving those tokens parked in escrow. Compliance is enforced on inbound bridge deliveries. Solana is exposed in the dApp at `https://rwa-testnet.onchainbridges.com` via the V1 C-lite path as of 2026-06-05 (gated by `VITE_SOLANA_ENABLED=true`, dApp component `SolanaBridgePanel.tsx`). The dApp uses `buildBridgeMessage` (V1 C-lite) with `compute_units = 0` to satisfy the FeeQuoter's hardened SVM destination address validation that rejects non-zero `gasLimit` with a zero receiver. The V2 atomic helpers (`buildBridgeMessageV2`, `encodeSvmExtraArgsV2`) stay in the codebase so the dApp can flip back to atomic delivery as soon as the Chainlink offramp update ships.

**C-lite trust-minimized recipient-claim path verified** (2026-05-20): the keeper-free v2 design (`ccip_receive` does atomic delivery) awaits a Chainlink Solana offramp update. The C-lite interim path was added to the deployed program: `PendingDelivery` PDA (seeded by CCIP message id), `record_pending_delivery` (admin-only, the interim writer), and `claim` (permissionless caller; the recipient signs to pull their tokens out of escrow through the hook). End-to-end on Devnet: 10 MBT bridged via the v1-style starter-kit send (CCIP message `0x8ebadc70639f2b429b87354777f4d029bd76ef300bd12282855fbfe5c8903aa8`), pool minted into escrow, admin recorded the pending delivery, **recipient self-signed `claim`** to receive 10 wrapped MBT through the compliance hook (escrow 14 → 4, recipient 6 → 16, PDA closed, rent refunded). The same claim flow will be used once the Chainlink offramp update ships; only the recorder changes. Solana is exposed in the dApp at `https://rwa-testnet.onchainbridges.com` via the V1 C-lite path as of 2026-06-05 (gated by `VITE_SOLANA_ENABLED=true`, dApp component `SolanaBridgePanel.tsx`). The dApp uses `buildBridgeMessage` (V1 C-lite) with `compute_units = 0` to satisfy the FeeQuoter's hardened SVM destination address validation that rejects non-zero `gasLimit` with a zero receiver. The V2 atomic helpers (`buildBridgeMessageV2`, `encodeSvmExtraArgsV2`) stay in the codebase so the dApp can flip back to atomic delivery as soon as the Chainlink offramp update ships.

## 6.9 Address book — quick reference

If you're integrating, the three addresses you'll hit most:

- **AllowPolicy** for the chain you're operating on (to call `addressAllowed(wallet)` for KYC checks)
- **MBT** address (the ERC-20 you read balances of)
- **For Sonic only:** `WrappedMBT v2` (no separate AllowPolicy — `addressAllowed` is a method on this contract directly)

## 6.10 Account Abstraction (AA) contracts

> AA Phase 2 (paying source-chain gas, and in v2 the CCIP LINK fee, in TLPT) is deployed on testnet but **not yet enabled in the dApp** — the "Gas mode" toggle is hidden behind `VITE_AA_V2_ENABLED` until the single-fee abstraction is complete (CLAUDE.md invariant 4). These contracts are live on-chain but are not yet a user-facing surface.

Authoritative source: `webapp/src/config/aa.ts`. Astar Shibuya is excluded (Pimlico does not support it).

**Canonical — identical on every chain:**
- EntryPoint v0.7: `0x0000000071727de22e5e9d8baf0edac6f37da032`
- SimpleAccountFactory v0.7 (Pimlico): `0x91e60e0613810449d098b0b5ec8b51a0fe8c8985`

Per chain: **TLPTPaymaster v1** (TLPT covers source-chain gas only; live since 2026-04-27) and **v2.1** (TLPT covers gas + CCIP LINK fees; deployed 2026-05-10), the **TLPT** fee token, and the **TLPTFaucet**.

### Sepolia
- TLPTPaymaster v1: `0xcaa55642befbaf6301be79dac88487ebe665ed6f`
- TLPTPaymaster v2.1: `0xc4f407562b446f024ff9bdddb390d8a499552c82`
- TLPT token: `0x1ceaae761c87278acfbe33c89ec523b46fabccf3`
- TLPTFaucet: `0x13e32c97a1437a8965cd99a8c34e67bdee5f7cfa`

### Polygon Amoy
- TLPTPaymaster v1: `0xb689499ef68846ce3d6fd8bb5c92f9ec88f45073`
- TLPTPaymaster v2.1: `0xa861e26770ec5ddcf84f43f281d373368f6f7db3`
- TLPT token: `0x8f1bb564ef4c323350ce301e4a4e354f0fab15f9`
- TLPTFaucet: `0x6c61658cfe0e5794f739782433a8011a6107a570`

### Soneium Minato
- TLPTPaymaster v1: `0x670c3a58435cc13e9eda059f4093f31cedeef7f3`
- TLPTPaymaster v2.1: `0x854870d876b35b4b5da6ea39d6c3093a9f34f733`
- TLPT token: `0xc1734f3714fd3ac97bda42e4d71f05a4830d70b3`
- TLPTFaucet: `0xbf9206b3f6b335875a242899c472c2c440fba02f`

### Sonic Testnet
- TLPTPaymaster v1: `0xe5e1e4b594c343c1e9bac0730b25fd4ab21f7389`
- TLPTPaymaster v2.1: `0x50966e229c642c13f503627f1d9c6e327aa77ed8`
- TLPT token: `0x3bc55a7da74e027b6f363e12e6f4cfd0282e43f3`
- TLPTFaucet: `0xbf9206b3f6b335875a242899c472c2c440fba02f`

### Plume Testnet
- TLPTPaymaster v1: `0x2b7b6f835d9c416e84ce85f982d37b5a78fbe6d8`
- TLPTPaymaster v2.1: `0xf08a207bb7d0198356ed4fffd555ee7129e2b8f5`
- TLPT token: `0x48db3f62b6c7328fb742b4799654136794dbe2b4`
- TLPTFaucet: `0xf48f2683aea6e5c1f395eef71b012c3fd554a797`

> v2.0 paymasters (deployed 2026-05-09) are superseded by v2.1 and remain on chain; their addresses are in the `aa.ts` comments. Minato and Sonic currently share a TLPTFaucet address (`0xbf92…a02f`) — a deterministic-deployment coincidence, they are independent contracts on separate chains.

## 6.11 Stacks Testnet4: non-EVM (Category C, non-CCIP), Phase A

Stacks is a Bitcoin L2 with Clarity smart contracts, reached without CCIP (Category C). Phase A (the token + native compliance) is deployed; the bridge transport (Phase B) is not built yet. RPC: `https://api.testnet.hiro.so`. Deployed 2026-06-13 via the Stacks Explorer "Write & Deploy" sandbox with a Leather wallet (no CLI key). Source + tests live in the `OnchainBridges-Stacks` worktree under `clarity/`.

| Contract | Address |
|---|---|
| **stx-mbt** (SIP-010 wrapped MBT: compliance + bridge mint/burn) | `ST1RSK6GEJ4GP8QC1QNN91J1KW014FBZCMTAQDQZW.stx-mbt` |
| **sip-010-trait** (local SIP-010 trait) | `ST1RSK6GEJ4GP8QC1QNN91J1KW014FBZCMTAQDQZW.sip-010-trait` |

Deployer / owner / relayer / compliance-admin (genesis, all the same principal until reassigned): `ST1RSK6GEJ4GP8QC1QNN91J1KW014FBZCMTAQDQZW`. Stacks addresses use canonical c32check (not EIP-55).

`stx-mbt` is the Stacks-native equivalent of the EVM ACE AllowPolicy: an allowlist + pause guard (`assert-compliant`) runs at the top of every value-moving function (`transfer` both sides, `bridge-mint`, `bridge-burn`), since Clarity has no inheritance. Burns are recorded as queryable state (the `burns` map + `get-burn` read-only getter), so the planned return-path 2-of-3 quorum can read each burn via the bare-node `/v2/contracts/call-read` RPC on independent stacks-core nodes rather than Hiro's `/extended/*` events indexer.

**Status:** deployed + verified live (name / symbol / decimals 18 / supply 0 / roles / paused=false all read back correct via `call-read`). NOT post-deploy-configured (relayer still = deployer, allowlist empty) and NOT exposed in the dApp. Per `policy_non_ccip_chain_compliance.md`, Stacks ships in the UI only after the compliance stack is wired end-to-end through the bridge and `pre-demo-check.ts` is green for it. UNAUDITED, demo-grade. Charter: `docs/handoffs/STACKS-KICKOFF-2026-06-13.md`.

---

[Next → Security Model](07-security.md)
