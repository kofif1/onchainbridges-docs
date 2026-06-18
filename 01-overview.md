---
title: "Overview"
---

# 1. Overview

[← Back to index](README.md)

## The problem

Tokenizing a real-world asset is the easy part. **Distributing it to compliant investors across the chains they actually use** is where every existing platform breaks down.

Issuers face three forced trade-offs:

1. **Pick one chain or maintain N silos.** Either the asset lives on a single chain (cutting off most of the addressable LP base) or the issuer maintains parallel deployments — separate compliance, separate liquidity, separate cap tables.
2. **Compliance "at issuance" or "at every transfer".** Most platforms KYC at mint and then let the token trade freely. Regulators increasingly require allowlist enforcement on every transfer, including peer-to-peer and secondary-market trades.
3. **Bridges as an afterthought.** Generic cross-chain bridges have no concept of allowlist, pause, or revocation. The moment a token crosses a bridge, the issuer's compliance posture is gone.

## What we build

A protocol layer that lives natively on every supported chain and:

- **Issues a single token** (per asset) that's bridgeable to any supported chain via Chainlink CCIP and CRE
- **Enforces compliance at every transfer** — mint, peer-to-peer, marketplace, even cross-chain delivery — via the Chainlink ACE allowlist + pause framework
- **Provides off-the-shelf secondary markets** — yield stripping (PT/YT), lending vaults, marketplaces — all gated by the same compliance layer
- **Onboards new chains in days** rather than weeks, with a uniform compliance posture from day one

We are NOT an appchain. We do not ask issuers or their LPs to migrate to a new chain. We deploy where investors and capital already are, and connect those deployments through Chainlink's audited infrastructure.

## Who it's for

| Role | What we offer |
|---|---|
| **RWA issuers** | One contract suite, one compliance setup, distribution to every chain their LPs use. Plus secondary markets (yield + lending) out of the box. |
| **Chain partners** (Plume, Soneium, Astar, Sonic) | A reference RWA deployment with full ACE compliance: instant credibility for their RWA vertical. |
| **DeFi protocols** | A KYC-clean RWA-backed asset they can list as collateral or quote markets in, without re-implementing compliance themselves. |
| **Regulated investors** | One KYC, every chain. Wallet allowlisted on Sepolia? You can receive the asset on Sonic, trade it on Plume, post it as collateral on Amoy. |

## Pitch pillars

Three things distinguish the platform from generic tokenization tooling:

1. **Compliance-at-every-transfer.** Built on Chainlink ACE. Every transfer — including bridge mints on non-CCIP chains — checks the allowlist. We never have a chain where the token can move freely.
2. **Native multi-chain tokens.** Built on Chainlink CCT. The token is the same canonical asset on every chain, not a bunch of "wrapped" derivatives.
3. **Yield + lending out of the box.** PT/YT stripping and over-collateralized lending markets are part of the default deployment, not afterthoughts.

## What you'll find in the rest of these docs

- **[Architecture](architecture.md)** — the five components: Token Factory, Cross-Chain Engine, Compliance Engine, Servicing Engine, Issuer Control Plane
- **[Compliance Model](03-compliance.md)** — how Chainlink ACE works in our deployment, including the policy chain and admin operations
- **[Cross-Chain Routing](04-cross-chain.md)** - when the protocol uses CCIP vs CRE
- **[Integration Guide](05-integration-guide.md)** — for chain partners and dApps integrating with the protocol
- **[Contract Reference](06-contracts.md)** — live addresses on every testnet chain
- **[Security Model](07-security.md)** — keys, upgrades, threat model
