---
title: "Security Model"
---

# 7. Security Model

[← Back to index](README.md)

This page documents the threat model, key custody, upgrade paths, and known limitations of the testnet deployment. **Production posture will differ** — items marked with 🔧 indicate where mainnet hardening is required.

## 7.1 Trust assumptions

The protocol depends on three external trust roots:

1. **Chainlink CCIP DON** — for token transfers between CCIP-supported chains. Chainlink-audited, multi-validator, RMN risk monitoring.
2. **Chainlink CRE DON** — for token transfers from CCIP chains to non-CCIP chains (e.g. Amoy → Sonic). Newer infrastructure than CCIP; same DON-consensus model.
3. **Issuer / protocol owner key** — controls allowlist updates, pause, contract upgrades. **This is the most concentrated single point of trust** and the primary mainnet-hardening target. See §7.4.

Investors trust the issuer not to grief them via allowlist removal, and the issuer trusts Chainlink not to compromise the bridge layer. The `AllowPolicy` allowlist is a fully on-chain audit trail of who's been added/removed.

## 7.2 Threat model

### What the protocol defends against

| Threat | Defense |
|---|---|
| Non-KYC'd wallet receives RWA tokens | ACE allowlist gate on every transfer + every mint |
| Bridge spends a token without compliance check | Destination's allowlist is enforced at `bridgeMint` |
| Upgrade-key compromise on a wMBT contract | wMBT v2 is non-upgradeable on Sonic; CCIP chains have ACE proxy keys (🔧 mainnet: multisig) |
| Replay of a CRE bridge report | `processedLocks[nonce]` mapping prevents double-mint |
| Stale lane / compromised CCIP RMN | Chainlink's RMN auto-pauses suspicious lanes; ACE on destination side adds defense in depth |
| Bug in policy logic on one chain | PausePolicy on every chain provides emergency stop |
| Compromised marketplace / lending vault contract | The contract must itself be allowlisted; we only allowlist after review |

### What the protocol does NOT defend against

| Out of scope | Why |
|---|---|
| Underlying RWA legal/custody risk | Off-chain — depends on issuer setup |
| Investor private key compromise | Standard wallet hygiene; not a protocol concern |
| Front-end (dApp) compromise | dApp is a UI layer; on-chain compliance still enforced regardless |
| User-side phishing of allowlisted addresses | Standard concern; protocol can't validate that the holder of a key is the KYC'd person |

## 7.3 Key custody

### Testnet (current)

- **Single deployer EOA** (`0xFc99…d33c`) holds:
  - Solidity contract ownership (PolicyEngine, AllowPolicy, PausePolicy, every WrappedMBT, LockVault, YieldIssuer, LendingVault)
  - MINTER role on every BurnMintTokenPool / WrappedMBT
  - Workflow-owner key for the CRE workflow (governs the WASM workflow uploads)
- **Pimlico paymaster API key** in the dApp build (gasless meta-tx flow on Sepolia/Amoy/Plume)
- **WalletConnect project ID** (public, low-risk)

This is acceptable for testnet. It is **not** acceptable for mainnet.

### Mainnet (planned 🔧)

- **Multisig** (Safe or equivalent) for ownership of every policy + token + vault
- **Time-locked upgrade path** (e.g. 48h delay) for policy changes that aren't emergency-pause
- **Separate operational keys** for routine operations (allowlist additions) vs structural changes (upgrades, ownership transfers)
- **Signing keys distributed** across founders / advisors / a regulated custodian where appropriate

## 7.4 Upgrade paths

### CCIP chains — UUPS proxies

PolicyEngine, AllowPolicy, PausePolicy on Sepolia, Amoy, and Plume are UUPS-upgradeable proxies. (Shibuya's compliance stack is deployed on the same pattern but the dApp lane is currently hidden pending Chainlink confirmation of CCIP lane status.) Upgrade authority is the deployer EOA today; mainnet target is multisig. Upgrades preserve allowlist state and emit an event auditors can subscribe to.

### Non-CCIP chains — non-upgradeable

WrappedMBT v2 on Sonic is **deliberately non-upgradeable**. Trade-off: bug fixes require redeploy + migration; benefit: no upgrade key to compromise. See `RUNBOOK.md` for the cutover procedure used during the v1 → v2 migration.

### CRE workflow — re-deployable

The WASM workflow that powers the Amoy → Sonic bridge can be re-deployed to the DON. This is normal operations (e.g. pointing at a new CREBridgeConsumer after a destination redeploy) rather than a security-sensitive event. Workflow-owner key is the deployer's `CRE_ETH_PRIVATE_KEY`.

## 7.5 Known limitations & open items

1. **Sepolia <-> Shibuya CCIP lane currently dormant** - Plume's gas-budget issue was resolved by Chainlink on 2026-05-14 and Sepolia <-> Plume bridges are now delivering end-to-end. Shibuya, however, shows zero OffRamp events on-chain over the last 33 hours, indicating the DON is not processing the lane regardless of gas budget. Awaiting Chainlink confirmation of lane status (active / decommissioned / migrating to v1.6).
2. **Sonic Testnet RPC has no CORS** — dApp can't read Sonic state from the browser, so destination-TX detection uses a deterministic Sonicscan deep-link instead of live polling. See RUNBOOK.md gotcha #3 (internal ops, not public).
3. **Sonic outbound bridging is not deployed** — bridges are one-way (in only) for Sonic until a return-side CRE workflow is built.
4. **MetaMask Amoy gas glitch** — patched in dApp via explicit `maxFeePerGas` override.
5. **CI is currently red** — yield + paymaster precision tests need updating after the YieldIssuer snapshot fix. Doesn't affect production state, but blocks branch merges.
6. **No formal audit yet** — testnet deployment uses Chainlink-audited components (CCIP, CRE, ACE) plus our thin layer (RWAToken, WrappedMBT v2, LockVault, CREBridgeConsumer, YieldIssuer, LendingVault, YTMarket). Mainnet ship requires audit of the thin layer.

## 7.6 Reporting a vulnerability

This is a testnet deployment with no live user funds. If you find a security issue, file a private GitHub Security Advisory on the repository, or contact the team via the email listed at https://onchainbridges.com.

---

[← Back to index](README.md)
