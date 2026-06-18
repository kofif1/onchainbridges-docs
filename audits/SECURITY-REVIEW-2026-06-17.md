---
title: "Security Review"
---

# Onchain Bridges - Automated Security Review (all networks: EVM + Solana + Stellar)

**Date:** 2026-06-17
**Reviewer:** RWA Bridge engineering (automated static analysis + manual triage)
**EVM compiler:** Solc 0.8.24, optimizer on (200 runs)
**EVM tools (three independent free/open-source analyzers):** Foundry `forge lint` v1.7.1, Cyfrin `aderyn` v0.1.9 (63 detectors), `solhint` (recommended ruleset)
**Solana tools:** `cargo audit` (RustSec advisory DB) + structural review of the Anchor programs
**Raw output:** [`aderyn-raw`](aderyn-raw-2026-06-17.md), [`forge-lint-raw`](forge-lint-raw-2026-06-17.txt), [`solhint-raw`](solhint-raw-2026-06-17.txt), [`solana-cargo-audit`](solana-cargo-audit-2026-06-17.txt)

> **Status:** This is an automated source-based review (the same static-analysis tools a
> professional auditor runs as a first pass) plus manual triage of every flagged item. It is a
> pre-audit technical review for grant due-diligence. It does **not** replace a full manual
> smart-contract audit, which remains required before any mainnet deployment.

---

## 0. Why the "free scanner" score looks bad (and why it is the wrong tool)

The public link that returned a low score - `solidityscan.com/quickscan/<addr>/etherscan/sepolia`
- is **SolidityScan QuickScan**, whose own title is "Free Threat Scanner & **Rug Pull Detector**."
It is a mainnet-trader-safety product. It scores a token on rug-pull heuristics: *can the owner
mint? can the owner pause? is there an allowlist? are there transfer hooks/fees?*

Onchain Bridges' RWA token (MBT) is a **compliance token**: owner-gated mint, pause, and an
allowlist are the entire point (the Chainlink ACE compliance stack). A rug-pull detector reads
every one of those controls as a red flag, so a compliance token will *always* score poorly on
QuickScan. **That score measures rug-pull surface, not code security**, and is not an
appropriate metric for a regulated-asset protocol. The findings below are the code-security view.

---

## 1. Scope

**This review covers every live network**, not just Sepolia. The EVM protocol is a single Solidity
codebase deployed across all EVM chains (Sepolia, Polygon Amoy, Sonic, Soneium Minato, Plume), so
the source-based EVM analysis below applies identically to every EVM deployment - the same source
compiles to the same bytecode on each chain. Per-chain on-chain verification status (which explorer
shows verified source for each address) is tracked in
[`../CONTRACT-VERIFICATION-AUDIT-LEDGER.md`](../CONTRACT-VERIFICATION-AUDIT-LEDGER.md). Solana is a
separate Rust/Anchor codebase and is reviewed in section 7.

The EVM analysis below was run against the canonical contracts (the 15 verified on Sepolia plus the
per-chain equivalents).

**Onchain Bridges custom code reviewed here:** RWATokenCCT (MBT), CrossChainBridge, YieldIssuer,
YieldToken, YTMarket, LendingVault, TLPTFaucet, ERC20MintExtractor.

**Third-party audited code (in scope as deployed, but authored + audited by Chainlink), not
re-audited here:** BurnMintERC677 (TLPT), BurnMintTokenPool (CCIP), PolicyEngine / AllowPolicy /
PausePolicy (Chainlink ACE), ERC1967Proxy (OpenZeppelin). A large majority of the deployed
bytecode is audited Chainlink / OpenZeppelin library code.

**Excluded:** the TLPTPaymaster (v1/v2) contracts - AA Phase 2 is feature-flagged off and not
live in the public dApp, so they are not part of the live surface this review certifies.

---

## 2. Result summary

| Severity | In live in-scope contracts | Notes |
|---|---|---|
| Critical | **0** | |
| High | **0 real** | 4 detector "High" items, all triaged to false-positive or out-of-scope (s.3) |
| Medium | **0** | |
| Low / Informational | code-quality + by-design only | centralization (compliance controls), style, gas (s.4) |

All three EVM analyzers agree there are **no security vulnerabilities**:
- `forge lint`: 19 items, all in two low/informational classes (`block.timestamp` comparisons and
  guarded `unsafe-typecast`), each confirmed benign (s.4).
- `aderyn` (63 detectors): 0 real High after triage (s.3), Low/Informational only (s.4).
- `solhint` (recommended ruleset): **0 errors**; the warnings are documentation
  (missing NatSpec, ~80%), gas optimizations, and naming/import style - no security findings.

---

## 3. Triage of Aderyn "High" findings (4)

None are exploitable vulnerabilities in the live contracts.

| ID | Title | Where | Disposition |
|---|---|---|---|
| H-1 | Arbitrary `from` in `transferFrom` | TLPTPaymaster, TLPTPaymasterV2 | **Out of scope** (paymaster, flag-off). Also the intended ERC-4337 pattern: the paymaster pulls the user's TLPT after `validatePaymasterUserOp` authorizes the userOp. |
| H-2 | Contract name reused across files | TLPTPaymaster(V2), TLPTFaucet, TLPTSale | **Not a vulnerability.** A code-organization detector (same interface/contract name appears in multiple files). No security impact. |
| H-3 | Uninitialized state variables | YieldIssuer `currentPeriodId`, LendingVault `nextPositionId`, YTMarket `nextListingId`, LockVault `lockNonce` | **False positive.** All four are auto-incrementing counters / nonces that are *designed* to start at 0. Zero is the correct initial value. |
| H-4 | Locks Ether without withdraw | TLPTPaymaster, TLPTPaymasterV2 | **Out of scope** (paymaster). A 4337 paymaster intentionally holds an ETH gas deposit in the EntryPoint; withdrawal is via the EntryPoint, not the contract. |

---

## 4. Low / informational findings

These are standard static-analysis quality, gas, and style notes. None is a vulnerability.

- **L-1 Centralization risk (trusted owner)** - **by design.** Owner-gated mint, pause, and
  allowlist are the compliance mechanism (Chainlink ACE). Documented and intentional for a
  regulated-asset protocol. This is the same control set a rug-pull scanner mis-reads as risk.
- **L-2 Unsafe ERC20 ops** - our tokens are known/trusted (MBT, TLPT, the test USDC); reverting
  ERC20s. SafeERC20 is a hardening recommendation, not an active bug. Candidate for a follow-up.
- **L-3..L-13** - wide pragma, `address(0)` checks on setters, `public`->`external`, magic
  numbers -> constants, `indexed` event fields, `nonReentrant` modifier ordering, PUSH0
  portability, single-use modifiers, scientific notation, an unused custom error, a redundant
  statement. All informational / gas / style. Tracked as a code-quality backlog; none gates the
  testnet surface.
- **`forge lint`:** `block.timestamp` comparisons (faucet cooldown, feed staleness, yield-period
  and interest timing - second-level manipulation is immaterial to all of these) and
  `unsafe-typecast` (e.g. RWATokenCCT `uint256(reserves)` is guarded by a `reserves <= 0` check;
  CrossChainBridge `uint8(48 + value%10)` is digit-to-ASCII, always in range). All benign.

---

## 5. Per-contract posture (live Sepolia)

| Contract | Critical/High/Med | Notes |
|---|---|---|
| MBT (RWATokenCCT) | 0 | 2 benign lint items (guarded cast, feed staleness) |
| CrossChainBridge | 0 | 1 benign lint item (ASCII conversion) |
| YieldIssuer | 0 | H-3 = intentional counter |
| YieldToken (YT-MBT) | 0 | lint-clean |
| YTMarket | 0 | H-3 = intentional counter |
| LendingVault (Meridian) | 0 | H-3 = intentional counter |
| TLPTFaucet | 0 | cooldown timestamps (benign) |
| TLPT (BurnMintERC677) | n/a | Chainlink-audited library code |
| ACE PolicyEngine/AllowPolicy/PausePolicy | n/a | Chainlink-audited library code |
| BurnMintTokenPool | n/a | Chainlink-audited library code |

---

## 6. Solana programs (Rust / Anchor)

The Solana side is a separate Rust/Anchor codebase: three programs under `solana/programs/` -
`mbt-defi` (820 LoC), `mbt-bridge-delivery` (650 LoC), `mbt-allowlist-hook` (331 LoC) - implementing
the DeFi logic, the cross-chain delivery receiver, and the Token-2022 transfer-hook compliance gate.
Program IDs are in `webapp/src/config/solana.ts`; source is public in the repo.

**Method:** `cargo audit` (RustSec advisory database) on the locked dependency tree + a structural
review of access control. (There is no free Slither-equivalent for Solana; cargo-audit + Anchor's
account-constraint model + manual review are the free-tool baseline.)

**Findings:**
- **Dependency advisories (cargo audit):** the flagged advisories (`atty`, `borsh 0.9.3`, `rand 0.7.3`,
  etc.) are all in **transitive crates pulled in by the Solana/Anchor toolchain**, not in our program
  code. They are the standard advisory set every Solana program inherits (host/build-time crates and
  niche serialization edge cases), not exploitable in the on-chain program context. Raw output:
  [`solana-cargo-audit-2026-06-17.txt`](solana-cargo-audit-2026-06-17.txt).
- **Access control:** strong. The programs use Anchor account constraints throughout - 33 / 51 / 19
  `has_one`/authority checks in mbt-defi / bridge-delivery / allowlist-hook respectively, with `Signer`
  constraints on privileged instructions. This is the idiomatic, audited Anchor pattern.
- **Arithmetic:** `overflow-checks = true` is set in the release profile, so any arithmetic overflow
  reverts the transaction (mitigating the sparse explicit `checked_*` usage).
- **Note:** full verifiable-build verification (matching on-chain bytecode to source via `solana-verify`)
  is a separate, heavier step not performed here; the program IDs and source are public for inspection.

No exploitable findings were identified in our Solana program code by this review. A professional
manual audit is still recommended before mainnet, same as the EVM side.

---

## 7. Stellar programs (Rust / Soroban)

A separate Rust/Soroban codebase: six contracts (`soroban/<crate>/`, commit `7d46c531`) - sMBT
(SEP-41 compliance token), sUSDC (demo stablecoin), LendingVault (Polaris), YieldIssuer, YT, YTMarket.
36/36 native tests green. Reviewed by the Stellar session per the uniform non-EVM standard set here
and recorded by session 5.

**Verification:** Soroban has no explorer "verified source" tab. Each contract's source builds
deterministically (`stellar contract build && stellar contract optimize`, stellar-cli 26.1.0, target
`wasm32v1-none`) to a WASM whose sha256 matches the on-chain code hash; each was confirmed via
`stellar contract fetch` + sha256. Hashes are in the [ledger](../CONTRACT-VERIFICATION-AUDIT-LEDGER.md).

**Method:** `cargo audit` + `cargo clippy --target wasm32v1-none` + per-contract access-control review.

**Findings (overall 0 Critical / 0 High / 0 Medium):**
- **cargo audit:** 0 vulnerabilities. Two "unmaintained" advisories (`derivative`, `paste`) are
  transitive via `soroban-sdk`, not our code - informational.
- **cargo clippy:** 0 errors; cosmetic only (a `manual_saturating_arithmetic` suggestion on a
  functionally-identical `checked_sub().unwrap_or(0)`, and one doc-indent).
- **Access control:** sMBT separates admin / compliance_admin / relayer roles; `bridge_mint` is
  relayer-auth + not-paused + lock-nonce replay-guarded + allowlist-checked; all SEP-41 paths
  require_auth + check allowlist on both sides. LendingVault: admin-only price/LTV, borrower-auth'd
  borrow/repay with LTV + liquidity guards, no admin drain path. YieldIssuer: issuer-only period
  lifecycle, holder-auth'd claims with double-claim guards, sole YT minter. YT: mint gated to the
  YieldIssuer + allowlist; every value path transitively gated on sMBT's KYC/pause state. YTMarket:
  permissionless over the gated token, compliance preserved transitively (a non-KYC buyer reverts on
  the YT-to-buyer leg). sUSDC is an intentionally-ungated demo asset.
- **Disclosed trust assumptions (not findings):** admin/relayer/issuer keys are trusted testnet-ops
  keys; LendingVault is demo-grade (fixed 1:1 price, no oracle/liquidation) and would need an oracle
  + liquidation for mainnet.

No exploitable findings in our Soroban contract code. The EVM-side bridge helper deployed for the
Stellar lane (label "StellarLockVault", address on Amoy) is `src/bridge/LockVault.sol`, already
covered by the EVM analysis in sections 2-5.

---

## 8. Conclusion

Across the live EVM protocol contracts, three independent open-source analyzers (forge lint,
Aderyn with 63 detectors, and solhint) **agree there are no exploitable Critical, High, or Medium
findings**. Every "High" the tools raised is a false positive (intentional zero-initialized
counters), a non-security code-org note, or an out-of-scope paymaster item. Remaining items are by-design compliance centralization plus a
standard code-quality / gas backlog. The compliance-heavy machinery (token, pools, ACE policies)
is audited Chainlink / OpenZeppelin code.

A full manual audit by a professional firm is still required before mainnet; this review covers
the testnet surface for grant due-diligence.

_Prepared 2026-06-17 by RWA Bridge session 5. All tools are free / open-source - no paid service
used. Reproducible at repo HEAD: `forge lint src/`, `FOUNDRY_EVM_VERSION=cancun aderyn .`,
`npx solhint 'src/**/*.sol'`, and `cd solana && cargo audit`._
