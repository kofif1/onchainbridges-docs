---
title: "Canton Integration"
---

# Onchain Bridges - Canton Integration

**Status:** this runs on Canton **TestNet** and is exercised through the public testnet dApp at
https://rwa-testnet.onchainbridges.com. It is demo-grade and **not audited**. No part of it runs on
Canton MainNet.

Onchain Bridges is a compliance and interoperability layer for tokenized real-world assets (RWAs).
**This page is Canton-specific**, and it describes one capability: how a KYC verification a holder
has already completed on an EVM chain is recognised for a Canton party that holder has proved
control of.

---

## 1. The capability

**A credential verified on an EVM chain is recognised for a Canton party, without the holder
repeating the verification.**

That is the whole of it. A holder who has completed our KYC journey once, on an EVM chain, can
prove control of a particular Canton party by signing with its key. That party is then recorded in
the same identity record as the verified EVM wallet, and our service will recognise it.

Why it matters: a holder who moves between chains should not have to repeat an identity check they
have already passed, and the applications they deal with should not each have to run their own.

---

## 2. What the holder does

1. Completes the KYC journey once, on an EVM chain. This is the existing journey, unchanged.
2. Proves, on our signer page at `canton-signer.onchainbridges.com`, that they control the Canton
   party they are claiming.
3. That party is then recorded in the same identity record as the verified EVM wallet.

Step 2 happens **off the ledger**: the holder sends no transaction and pays no gas.

---

## 3. The signing key on the signer page

A Canton party can be created on our signer page, in the holder's own browser. That page states,
verbatim:

> "Your signing key is created in this browser and is never sent to any server. It leaves the
> browser only inside your backup file, encrypted with your passphrase - keep that file safe."

**Scope:** that describes a key created on the signer page. It does not describe any Canton party
that was not created on the signer page, including parties hosted on a participant node, ours or
another operator's; key custody for such parties is whatever their own creation and hosting
arrangements provide.

---

## 4. How current the recognition is

The recognition is not a flag written once and then trusted. **Status is checked at the time of each
request**, by reading the holder's verification status on the chain that holds it (the Sepolia
testnet).

That status read is the only part of this that is current by construction. It is not a revocation
mechanism, and section 5 says what it does not reach.

---

## 5. Limits, stated plainly

These are real limits of the integration as it stands, not caveats about future work.

- **Revocation does not propagate across chains, and it is not automatic.** Withdrawing a
  verification at the identity provider does not, by itself, reach any chain.
- **A withdrawn holder is not removed by the withdrawal.** The status read in section 4 will report
  them as not currently verified, but two other things persist until a person changes them by hand:
  the service's own list of parties it will serve is **grant-only**, with no re-check and no removal
  path in the code, and admission to an asset's allowlist is a **manual operation**. Neither lapses
  on its own.
- **Not every Canton party can use this.** The service maintains its own list of parties it will
  serve, and a party outside that list is refused even if the holder behind it is verified.
- **The link and the verification are not written to the Canton ledger.** They are held off the
  ledger, so nothing on Canton can read the link directly. This is not a claim that Canton holds no
  record of the holder: an asset's allowlist is an on-ledger list of admitted parties, and a Canton
  party id carries a holder-chosen name fragment that is visible in network topology.
- **One party per link.** What is recognised is the specific Canton party the holder proved control
  of. It does not extend to other parties the same holder may control.
- **Custody of the asset follows a registrar model.** The party that administers an asset in this
  integration holds authority over holdings of it. Nothing on this page should be read as a
  statement that only the holder can affect their holding.
- **TestNet only, and not audited.** See the status note at the top of this page.

---

## 6. What this is not

- It is **not** a credential on Canton. No credential is issued on, or held by, the Canton ledger.
- It is **not** a claim that the holder is verified under any particular jurisdiction's rules. What
  is recognised is that our KYC journey was completed, nothing more.
- It is **not** an onboarding or admission decision made by Canton or by any Canton application.
  Each application decides for itself what to do with the recognition.

---

## 7. Where to see it

The flow runs in the public testnet dApp at https://rwa-testnet.onchainbridges.com, with the Canton
party proof on the signer page named in section 2.
