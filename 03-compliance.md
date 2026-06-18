---
title: "Compliance Model"
---

# 3. Compliance Model

[← Back to index](README.md)

The protocol's central pillar: **compliance is enforced at every transfer, on every chain, with no escape hatches**. This page explains how that works in practice.

## 3.1 The principle

A regulated RWA token cannot move between two non-KYC'd wallets. Period. This applies to:

- Direct `transfer` and `transferFrom` calls
- Mints — including bridge-driven mints from another chain
- Marketplace trades — buyer and seller both checked
- Lending and yield-stripping operations

If any party in a transfer is not on the allowlist, the call reverts at the token level. There is no bypass at the marketplace level, no "trusted operator" exception, no time-locked grace period.

## 3.2 How it's enforced — Chainlink ACE

On CCIP-routed chains, we use the **Chainlink Asset Compliance Engine (ACE)**:

```
┌────────────────────────┐  per-call hook  ┌──────────────────────────┐
│  RWAToken (ERC-20)     │ ──────────────► │   PolicyEngine (UUPS)    │
│  PolicyProtected       │                 │                          │
└────────────────────────┘                 │   per-(token, selector): │
                                           │     ▶ AllowPolicy        │
                                           │     ▶ PausePolicy        │
                                           └──────────────────────────┘
```

On every `transfer`, `transferFrom`, and `mint`, the token contract calls `policyEngine.run(payload)`. The engine looks up the registered policies for that (token, selector) pair and runs each. If any policy reverts, the entire transfer reverts.

**Default policy set:**
- **AllowPolicy** — both sender and receiver (or the recipient, for mints) must be on the per-policy allowlist
- **PausePolicy** — global circuit breaker for the token

**Owner-controlled admin:**
- `AllowPolicy.allowAddress(account)` — add a wallet
- `AllowPolicy.disallowAddress(account)` — remove a wallet
- `AllowPolicy.allowAddresses([...])` — batch
- `PausePolicy.setPaused(true|false)` — emergency stop

**Where to find allowlist contracts per chain:** see [Contract Reference](06-contracts.md).

## 3.3 Non-CCIP chains — same semantics, simpler stack

Chains reached via Chainlink CRE or future additional routing providers don't natively run the ACE PolicyEngine. They host a **WrappedMBT v2** which inlines the same compliance semantics into a single contract:

```solidity
function _checkCompliance(address from, address to) internal view {
    if (paused) revert ContractPaused();
    if (from != address(0) && !allowlist[from]) revert NotAllowlisted(from);
    if (to != address(0) && !allowlist[to]) revert NotAllowlisted(to);
}
```

Called on every state-changing function: mint, burn, transfer, transferFrom. The same allowlist mappings, the same admin functions (`allowAddress` / `disallowAddress` / `allowAddresses` / `setPaused`).

We chose inlined enforcement over a full PolicyEngine deployment for non-CCIP chains because:

1. **No upgrade key on the contract** — non-upgradeable means no proxy admin to compromise
2. **Single contract, ~50 LOC of new compliance code** — minimal attack surface
3. **Impossible to misconfigure** — the check sits inside `_update`-equivalent paths, every state change goes through it; there's no "forgot to attach a policy to a selector" failure mode

The economic and regulatory effect is identical to the full ACE stack.

## 3.4 KYC mirroring — adding a new investor

Today, when a wallet is KYC-approved, it must be added to the allowlist on **every chain** the protocol operates on. The `cast` commands for this batch are in Operations Runbook (internal ops, not public) §3.C.

### Future: automatic mirroring

The roadmap is for ACE itself to surface a **KYC credential** that any chain's allowlist can read off-chain or via a credential proof. When that ships, the CRE workflows (and any future additional routing providers) can auto-allowlist a recipient at bridge-mint time, eliminating manual mirroring.

Until then, manual mirroring is the rule. Missing it on one chain means the wallet can't receive bridged tokens there — the bridge mint will revert at `_checkCompliance`.

## 3.5 What this gives investors

A wallet that's been KYC-approved can:

- Receive the RWA token on any supported chain
- Send to any other allowlisted wallet (peer-to-peer or via marketplace)
- Bridge between chains without losing compliance
- Use the token in the lending and yield products

A wallet that has **not** been KYC-approved cannot interact with the token at all — receive, send, or hold it. Attempts revert. There is no greylist, no probationary period, no "small amount" exception.

## 3.6 Pause behavior

`PausePolicy.setPaused(true)` (or `WrappedMBT.setPaused(true)` on non-CCIP chains) freezes all token movement instantly. Used for:

- Asset-level recall events (e.g. underlying RWA event that requires holding)
- Investigation / breach response
- Coordinated upgrade windows

A paused token is non-transferable. Existing balances are preserved. Reads (balanceOf, etc.) still work.

---

[Next → Cross-Chain Routing](04-cross-chain.md)
