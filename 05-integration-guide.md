---
title: "Integration Guide"
---

# 5. Integration Guide

[← Back to index](README.md)

This section covers how to integrate as a chain partner, dApp, or ancillary service. For investor-side use (KYC, wallet onboarding, holding assets), see the public dApp at https://rwa-testnet.onchainbridges.com.

## 5.1 For chain partners (Plume, Soneium, Astar, Sonic, etc.)

If you operate or work with an EVM-compatible chain and want a reference RWA deployment with full compliance, here's how onboarding works.

### What you get

A complete deployment of:
- The asset's RWA token with cross-chain bridging to any other supported chain
- Compliance gating identical to every other chain in the protocol (no second-class chains)
- Lending vault accepting the RWA token as collateral
- Yield stripping (PT/YT) and YT marketplace
- Listing in the dApp's chain selector — one-click bridging from any other chain

### What we need from you

| Item | Why |
|---|---|
| EVM-compatible RPC (HTTPS, ideally CORS-enabled) | dApp reads on-chain state from the browser |
| Block explorer URL | Surface TX hashes from the bridge UI |
| Native gas-token faucet (testnet) | Investor wallets need gas for transfers |
| Either: (a) CCIP support, OR (b) ability to operate a CRE workflow targeting your chain | Choose tier 1 vs 2 routing |

### Integration steps

1. **RPC + chain config** — we add your chain to `webapp/src/config/chains.ts` (single source of truth) and the wagmi connector list
2. **Compliance stack deploy** — either full Chainlink ACE (PolicyEngine + AllowPolicy + PausePolicy proxies) or the equivalent inlined in our `WrappedMBT v2` pattern. Decision criteria:
   - If your chain is on CCIP → full ACE, native MBT, BurnMintTokenPool
   - If non-CCIP → inlined `WrappedMBT v2` + CRE workflow targeting the chain
3. **Servicing contracts** — LendingVault + YieldIssuer + YT marketplace deployed and wired to the compliance stack
4. **Bridge wiring** — either (a) CCIP lane registration (Chainlink does this on their side; we provide token + pool addresses), or (b) CRE workflow deployment with your chain in `project.yaml` rpcs
5. **Allowlist seeding** — bootstrap addresses (deployer, our protocol contracts, your test wallets, partner wallets)
6. **dApp listing** — add your chain to the selector, run `webapp/pre-demo-check.ts` until all green
7. **Public verification** — end-to-end test bridge from at least one other chain, surface explorer link

Typical timeline: **3–5 working days** for a CRE-routed integration, depending on RPC + faucet availability. CCIP integration is gated by Chainlink's lane-onboarding pace, typically 1–3 weeks.

### Compliance posture is non-negotiable

We will not enable a chain in the bridge dropdown until it has equivalent compliance gating to the rest of the protocol. This is a **hard rule** — see `memory/policy_non_ccip_chain_compliance.md` (private) for the reasoning. A chain with vanilla ERC-20 wMBT cannot ship under our protocol.

This rule benefits chain partners too: if you're hosting our deployment, every transfer of the RWA token on your chain enforces the same KYC posture as every other chain. Your regulators see the same compliance model.

## 5.2 For dApps (DeFi protocols, marketplaces, etc.)

The RWA token is a standard ERC-20 with **one extra reverting condition**: transfers to/from non-allowlisted wallets revert. As a dApp integrator, here's what changes vs a vanilla ERC-20:

### Read pattern

Same as ERC-20. `balanceOf`, `totalSupply`, `decimals`, etc. work normally.

### Write pattern — additional check

Before any contract that calls `transferFrom` or `transfer` on behalf of a user, the user's wallet AND the contract itself must be on the AllowPolicy allowlist for that chain.

**For your contract:** request allowlisting from the RWA issuer. Provide:
- Contract address
- Chain
- Brief description of what the contract does

We add it via `AllowPolicy.allowAddress(yourContract)`. From then on, transferFrom calls originating from your contract execute normally.

**For your users:** they must complete the issuer's KYC to be on the allowlist before they can hold or move the token. This is the same requirement as buying the token directly; you're not creating a new compliance burden.

### Detecting allowlist status from the front-end

```ts
// Per-chain — see Contract Reference for addresses
const allowPolicy = "0x..."; // AllowPolicy address for this chain
const allowed = await publicClient.readContract({
  address: allowPolicy,
  abi: ["function addressAllowed(address) view returns (bool)"],
  functionName: "addressAllowed",
  args: [userWallet],
});
// If !allowed, surface "wallet not allowlisted — complete KYC at <issuer>"
```

### Pause posture

Your dApp should be defensive about the token being paused — `paused()` on the PausePolicy returns `true` during a pause. While paused, all transfers revert. Surface "trading currently paused by issuer" rather than treating the revert as a bug.

## 5.3 For ancillary services (analytics, oracles, indexers)

Standard ERC-20 events apply: `Transfer`, `Approval`. Plus `BridgeMint(lockNonce, to, amount)` on non-CCIP chains' wMBT contracts for tracking cross-chain delivery.

Allowlist events for indexing KYC state changes:
- `AllowPolicy.AddressAllowed(account)`
- `AllowPolicy.AddressDisallowed(account)`
- `WrappedMBT.AllowlistSet(account, allowed)` — non-CCIP variant
- `PausePolicy.PauseStateChanged(paused)`

Subscribe to these to keep an off-chain copy of compliance state in sync.

---

[Next → Contract Reference](06-contracts.md)
