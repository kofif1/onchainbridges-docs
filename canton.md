---
title: "Canton Integration"
---

# Onchain Bridges - Canton Integration

**Status:** this runs on **Canton TestNet** and is exercised through the public testnet dApp at
https://rwa-testnet.onchainbridges.com. It is demo-grade and **not audited**. No part of it runs on
Canton MainNet.

<div data-video-id="4eC7cMQ1Wys" style="max-width:720px;margin:28px 0">
  <button type="button" style="border:0;padding:0;background:#000;cursor:pointer;display:block;width:100%;position:relative;border-radius:12px;overflow:hidden">
    <img src="assets/canton-demo-thumbnail.png" style="display:block;width:100%;height:auto"
         alt="A recorded walkthrough of this flow on TestNet (video).">
    <span style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:92px;height:64px;border-radius:14px;background:rgba(220,0,0,.92);display:flex;align-items:center;justify-content:center">
      <span style="display:block;width:0;height:0;border-left:26px solid #fff;border-top:16px solid transparent;border-bottom:16px solid transparent;margin-left:6px"></span>
    </span>
  </button>
</div>
<script src="assets/video-facade.js"></script>

Pressing play loads the video from YouTube.

Onchain Bridges is a compliance and interoperability layer for tokenized real-world assets. **This
page is Canton-specific:** what we have built on Canton, the identifiers you can verify it with, and
how the pieces fit together.

Canton matters to us because its privacy model is the opposite of a public EVM chain: contracts are
visible only to their stakeholders. An asset that moves to Canton has to carry its compliance with
it, and it has to do so without a public ledger to read.

---

## 1. What is on Canton today

- **MBT as a Canton instrument.** The same real-world-asset token the protocol uses on its EVM
  chains, issued on Canton TestNet through our own Daml instrument package, with a registry service
  (`ob-mbt-registry`) in front of it.
- **A CCIP lane from Sepolia to Canton.** A transfer burns on the EVM side and the corresponding
  amount appears as a holding on the Canton ledger. Canton is a CCIP destination with its own chain
  selector.
- **Allowlist screening on the instrument.** The instrument carries a list of admitted parties. A
  transfer to a party that is not admitted is refused.
- **A browser signer.** A Canton party can be created in the holder's own browser at
  `canton-signer.onchainbridges.com`. The key stays in the holder's browser, which signs.
- **KYC recognition.** A credential verified on an EVM chain is recognised for a Canton party the
  holder has proved control of, so the holder does not repeat the verification. Section 4 covers it.

---

## 2. Identifiers

Canton's privacy model means there is no public explorer to point at the way there is for an EVM
chain. These are the identifiers that name the deployment, so a counterparty we transact with can
confirm they are dealing with the same instrument and the same party we describe here.

### Canton TestNet

| What | Identifier |
|---|---|
| MBT instrument package | `ee08b2105cdfa1d0c78c242b6f6cc6abb93d56f8237f67cc8c72819e895d86ba` |
| Instrument admin party | `onchainbridges::12209e39d63409d30dc8f1fe4a27cbabdd32e4300e18b271d38dfdc319a4f4435928` |
| Synchronizer | `global-domain::1220f22a8b8f2d813c25b9a684dc4dd52b532a0174d8e73a13cdf2baabfff7518337` |
| Registry service | `ob-mbt-registry` |
| CCIP chain selector | `9268731218649498074` |
| MBT decimals on Canton | 10 |

A Canton party id is `<name>::1220<64 hex>`, where the second part is a fingerprint of the
namespace key. The `1220` prefix is a multihash header: `0x12` for SHA-256, `0x20` for its 32-byte
length.

### Sepolia (the EVM side of the lane)

| Contract | Address |
|---|---|
| MBT (RWATokenCCT) | [`0x3953a90Ad44Dc771E7A1a1Fc4608Bb89f13cA068`](https://sepolia.etherscan.io/address/0x3953a90Ad44Dc771E7A1a1Fc4608Bb89f13cA068) |
| MBT AllowPolicy | [`0x7858b6e699c381583A8A820F52AF051197B3DCD1`](https://sepolia.etherscan.io/address/0x7858b6e699c381583A8A820F52AF051197B3DCD1) |

Both are EIP-55 checksummed. The full cross-chain registry is in the
[Contract Reference](06-contracts.md).

---

## 3. How a transfer reaches Canton

1. The holder sends MBT from Sepolia through CCIP, naming a **Canton party id** as the recipient.
2. The party id is a string, not an address. The contract hashes it with `keccak256` and carries the
   result as the CCIP receiver, so the destination is committed to in the message rather than
   re-supplied later.
3. On arrival the amount appears as a holding of that party on the Canton ledger, denominated at
   10 decimals.
4. The instrument's allowlist screens the parties to the movement. A transfer to a party that is
   not admitted is refused.

**A limitation worth knowing before you design around it.** Delivery to a party we do not host
requires a manual execution step on the Canton side; manual execution is how CCIP delivery to
Canton is designed, not a temporary outage. Where the receiving party is one we host, the leg
completes without operator involvement. We have not yet exercised the leg to a party hosted outside
our own participant, so a third-party integration should plan for the manual step rather than
around it.

---

## 4. One KYC, recognised for a Canton party

A holder who has completed our KYC journey once, on an EVM chain, can prove control of a Canton
party by signing with its key. That party is then recorded in the same identity record as the
verified EVM wallet, and our service recognises it. No second verification.

The proof is **off the ledger**: the holder sends no transaction and pays no gas. It is two
signatures over a single challenge, one from the EVM wallet and one from the Canton key.

Status is checked **at the time of each request**, by reading the holder's verification status on
the chain that holds it (the Sepolia testnet), rather than trusting a flag written once.

### The signing key

A Canton party can be created on our signer page, in the holder's own browser. That page states,
verbatim:

> "Your signing key is created in this browser and is never sent to any server. It leaves the
> browser only inside your backup file, encrypted with your passphrase - keep that file safe."

That describes a key created on the signer page. It does not describe any Canton party that was not
created there, including parties hosted on a participant node, ours or another operator's; key
custody for such parties is whatever their own creation and hosting arrangements provide.

---

## 5. Who controls what

**Canton follows a registrar model, and the distinction matters more here than on an EVM chain.**

For this instrument, the administering party is a signatory on holdings of it, which carries
issuer-side authority over those holdings. Onchain Bridges operates the instrument's register and
its compliance controls. **Nothing on this page should be read as a statement that only the holder
can affect their holding.**

What is true of the key material: for a party created on the signer page, the key is the customer's
own, in their browser, and Onchain Bridges holds no copy of it. For parties created or hosted by
other arrangements, key custody is whatever those arrangements provide.

---

## 6. Limits

- **Revocation does not propagate across chains, and it is not automatic.** Withdrawing a
  verification at the identity provider does not, by itself, reach any chain. A withdrawn holder is
  reported as not currently verified by the status read in section 4, but removal from the service's
  party list and from an asset's allowlist are operations a person performs.
- **Not every Canton party can use the KYC recognition.** The service maintains its own list of
  parties it will serve.
- **The link and the verification are not written to the Canton ledger.** They are held off it. An
  asset's allowlist is, however, an on-ledger list of admitted parties, and a party id carries a
  holder-chosen name fragment visible in network topology.
- **TestNet only, and not audited.**

---

## 7. Where to see it

The flow runs in the public testnet dApp at https://rwa-testnet.onchainbridges.com, with the Canton
party proof on the signer page named in section 4.
