---
title: "Documentation"
---

# Onchain Bridges Documentation

Interoperability and compliance infrastructure for tokenized real-world assets (RWAs). A single
token, the same KYC posture, on every chain a regulated investor wants to use, built on Chainlink
(CCIP, the Cross-Chain Token standard, the Automated Compliance Engine, the Runtime Environment,
and Proof of Reserve). Live testnet dApp: https://rwa-testnet.onchainbridges.com

## Protocol documentation
1. [Overview](01-overview.md), what the protocol does and who it is for
2. [Architecture](architecture.md), system layers and components
3. [Compliance Model](03-compliance.md), KYC enforced at every transfer via Chainlink ACE
4. [Cross-Chain Routing](04-cross-chain.md), how tokens move across chains (CCIP + CRE)
5. [Integration Guide](05-integration-guide.md), onboarding chains, issuers, and dApps
6. [Contract Reference](06-contracts.md), live testnet addresses across supported chains
7. [Security Model](07-security.md), threat model, key custody, upgrade paths

## Chain integrations
- [Canton Integration](canton.md), how a KYC verification completed on an EVM chain is recognised
  for a Canton party the holder has proved control of (Canton TestNet, demo-grade, not audited)

## Security review
- [Security Review](audits/SECURITY-REVIEW-2026-06-17.md), a static-analysis review of our own
  source (Foundry forge-lint + Cyfrin Aderyn + solhint + cargo-audit), dated 2026-06-17: no
  Critical, High or Medium findings in the contracts it covers. It is **not** an independent
  third-party audit, and it does not cover contracts deployed after its date. No formal audit has
  been commissioned; see [Security Model](07-security.md).
- [Verification and Audit Ledger](CONTRACT-VERIFICATION-AUDIT-LEDGER.md), every contract, every
  chain, with block-explorer links.

## Networks

The protocol is deployed natively across multiple public testnets. Full per-chain contract
addresses are in the [Contract Reference](06-contracts.md); the multi-chain design is in
[Architecture](architecture.md).

- **EVM testnets:** Ethereum (Sepolia), Polygon (Amoy), Soneium (Minato), Plume, Sonic, Astar (Shibuya)
- **Non-EVM:** Solana (Devnet), Stellar / Soroban
- **In progress:** Stacks (Bitcoin L2), bridge working, integration ongoing

Compliance (allowlist + pause enforced on every transfer) and the cross-chain bridge are
implemented natively on each chain, EVM and non-EVM alike.

---
_Status: pre-mainnet. Deployed and live on public testnets; a formal audit precedes mainnet._
