---
title: "Cross-Chain Routing"
---

# 4. Cross-Chain Routing

[← Back to index](README.md)

The protocol uses two production routing tiers today, each picked automatically based on the source/destination chain pair. The user always sees a single "Bridge" button: the underlying mechanism is invisible.

## 4.1 Tier overview

| Tier | Provider | Latency | Coverage | Lane status |
|---|---|---|---|---|
| 1 | **Chainlink CCIP** | ~10-30 min | CCIP-supported chains | Live: Sepolia, Polygon Amoy, Plume Testnet (Astar Shibuya temporarily removed, lane status pending Chainlink) |
| 2 | **Chainlink CRE** | ~15-30 sec | Any EVM-compatible RPC | Live: Amoy to Sonic Testnet |

Each tier has different operational and trust characteristics; we pick the strongest available for any given chain pair.

## 4.2 Tier 1 — Chainlink CCIP

**Used for:** chain pairs where both source and destination are part of CCIP's audited lane network.

**How it works:**
1. User calls `Router.ccipSend(message)` on the source chain
2. Source `BurnMintTokenPool` burns the user's MBT
3. CCIP DON observes the burn, reaches consensus, signs a report
4. Destination `BurnMintTokenPool` mints fresh MBT to the receiver
5. Both burn and mint route through ACE; non-allowlisted receivers cause the destination mint to revert

**Strengths:**
- CCIP DON has full Chainlink-grade infrastructure: risk monitoring (RMN), per-lane audits, formal verification of pool contracts
- Native fee market (LINK or wrapped native) — predictable costs
- Same code path on every CCIP chain, so adding a new CCIP chain is just lane wiring

**Weaknesses:**
- Limited to chains Chainlink actively supports
- Latency ~10–30 min on testnet (faster on mainnet)
- Per-lane gas-budget tuning sometimes required for ACE-protected tokens. Plume's inbound budget was raised by Chainlink on 2026-05-14 and bridges are now delivering end-to-end. Shibuya's lane is currently dormant on the DON side (zero OffRamp events over 33h); status pending Chainlink confirmation before re-enabling.

## 4.3 Tier 2 — Chainlink CRE (Compute Runtime Environment)

**Used for:** chains that aren't on CCIP but have a working EVM-compatible RPC. **Sonic Testnet is the live example.**

**How it works:**

```
┌──────────────────┐                                    ┌────────────────────┐
│  Source: Amoy    │                                    │  Dest: Sonic       │
│                  │                                    │                    │
│  LockVault.lock  │  ─── emit Locked(nonce, ...) ──►   │  CRE Workflow (DON)│
│  (locks MBT)     │                                    │  picks up event    │
│                  │                                    │                    │
│                  │                                    │   ▼ DON consensus  │
│                  │                                    │   ▼ signed report  │
│                  │                                    │                    │
│                  │       ┌─────────────────────┐      │  KeystoneForwarder │
│                  │       │ CREBridgeConsumer   │ ◄─── │  delivers report   │
│                  │       │   _processReport    │      │                    │
│                  │       └──────────┬──────────┘      └────────────────────┘
│                  │                  │
│                  │                  ▼
│                  │       ┌─────────────────────┐
│                  │       │  WrappedMBT v2      │
│                  │       │   bridgeMint(to)    │
│                  │       │   — ACE allowlist   │
│                  │       │     enforced here   │
│                  │       └─────────────────────┘
└──────────────────┘
```

1. User calls `LockVault.lock(amount, destChainId, recipient)` on the source chain (Amoy)
2. LockVault locks the user's MBT (no burn — backing is preserved on the source) and emits a `Locked(nonce, ...)` event
3. A WASM workflow deployed to the CRE DON listens for `Locked` events. Once it sees one, it reaches consensus among the DON nodes and signs a report
4. `KeystoneForwarder` (the CRE-equivalent of CCIP's OffRamp) calls `CREBridgeConsumer._processReport` on the destination chain
5. The consumer calls `WrappedMBT.bridgeMint(recipient, amount, nonce)` — which checks both `processedLocks[nonce]` (replay protection) AND the recipient is allowlisted on the destination's compliance gate
6. wMBT lands in the recipient's wallet

**Strengths:**
- Sub-30-second delivery on testnet (vs CCIP's 10–30 min)
- Works for any EVM-compatible chain that the CRE DON can reach
- Same compliance semantics as CCIP — the destination's `_checkCompliance` (or PolicyEngine, when present) is enforced

**Weaknesses:**
- Less battle-tested than CCIP (CRE is a newer Chainlink product)
- Workflow code is custom per chain pair (though the template is reusable)
- Currently one-way only for Sonic — outbound (Sonic → other chains) requires a second workflow that's not yet deployed

**Operational notes:** see Operations Runbook (internal ops, not public) §3.B for the redeploy procedure.

## 4.4 Extensibility: additional routing tiers

**Intended use:** long-tail chains where neither CCIP nor a custom CRE workflow is the right fit, typically partner chains with strong RWA demand but limited Chainlink presence.

The routing layer is a swappable plug-in: any provider that can deliver an attested cross-chain message can be wired in behind the same Bridge button users already see. Sonic's CRE deployment is the validation case for our own per-chain template, an in-house route that needs no third party.

## 4.5 How the dApp picks the routing tier

The Bridge form's destination dropdown maps each chain to its routing tier:

| Destination | Tier |
|---|---|
| Sepolia, Amoy, Plume | CCIP |
| Sonic Testnet | CRE |

The tier choice is **invisible to the user**. They click "Bridge", the form switches to the right contract call automatically, and the status panel reports outcome the same way. Compliance is enforced consistently across all three.

---

[Next → Integration Guide](05-integration-guide.md)
