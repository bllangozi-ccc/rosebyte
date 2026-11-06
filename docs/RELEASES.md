# Owner-encrypted core releases

The current plaintext implementation is private. This fresh public repository contains guides, public specifications/examples, generic client SDK and owner-encrypted software. It contains neither the private release recipient nor an owner secret. The archive includes the native/reference engine, full source tests, hosted source without operational state and benchmark reproduction material. Service keys, owner vault, passkey records and account databases are excluded.

## Encryption boundary

The owner initialised a dedicated X25519 release recipient locally. Its private key is encrypted under the existing owner secret using scrypt and AES-256-GCM; the original owner vault is untouched. A fresh ephemeral X25519 exchange plus HKDF-SHA256 and AES-256-GCM seals every release to the public recipient. This permits automated future release encryption without giving the publisher the owner's secret. Only an authorised owner decryption session can unwrap the release recipient.

This is encryption at rest, not a way to revoke already decrypted source, and it does not retract earlier public copies. No private recipient is published. Keep its encrypted local backup as well as the secret; the secret alone cannot reconstruct a lost random recipient. Protect the secret against guessing. Signing into the website with a biometric/passkey is a separate operation.

## Verify this release on94

In the owner's root PuTTY session, run:

```sh
rb-release-key verify /work/jack/rosebyte-distribution/releases/rosebyte-core-0.10.0a1.rbenc
```

Enter the existing secret only at its hidden prompt, never in chat, a command argument or an environment variable. The command decrypts in memory and verifies authenticated content, declared size and SHA-256. It does not extract or run the core. A successful response says `verified`. The owner reported `verified` on 6 November 2026, with the expected 775070 bytes and matching hash prefix. This is an owner-reported recovery receipt, not an independent audit.

For an authorised reviewer, decrypt to a new private output file using `rb-release-key decrypt SEALED NEW-ARCHIVE`, then inspect the archive before extracting it into an empty private directory. Sharing decrypted material is a separate owner decision; encryption cannot prevent an authorised recipient copying it.

The [manifest](../releases/manifest-0.10.0a1.json) and [ciphertext hash](../releases/SHA256SUMS) identify the release. Check them through a trusted publisher channel: anyone with a public recipient key can encrypt different content, so encryption alone is not publisher authentication. Owner-only builds/tests are described in the native guide and Architect checklist. Public CI validates the distribution and its hashes; it does not pretend to execute an encrypted compiler.


## Native0.10.2a1 follow-up

The encrypted native-fix archive applies to a fresh copy of the original authorised source release and includes the reference equality correction, runtime Unicode guard, qualifiedjson-c0.19dependency, tests and original-before/after evidence. Native and reference package version0.10.2a1. This update is sealed to the existing owner-initialised recipient without asking for the secret again. The original owner-verified artifact remains unchanged. Current decoder qualification and platform limits are in REVIEW-FIXES.md and NATIVE.md; independent final retest remains pending. Third-partyjson-cnotices accompany the authorised release.

## Hosted guest chat update — 6 November 2026

Numbered read-only guest landing; registration and current-rule acceptance before public/private posting; earlier member history retained as member-only; private rooms remain isolated. Added canonical individual guide pages and generated sitemap. Fixed backup WAL sandbox coordination. 75 hosted tests and disposable browser scenarios pass. Hosted changes are provided as `rosebyte-guest-chat-20261106.rbenc`, sealed to the existing owner release recipient. Native language 0.10.2a1 and its measured codec results are unchanged.
