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

Enter the existing secret only at its hidden prompt, never in chat, a command argument or an environment variable. The command decrypts in memory and verifies authenticated content, declared size and SHA-256. It does not extract or run the core. A successful response says `verified`. Actual owner verification of this archive is pending until that command succeeds.

For an authorised reviewer, decrypt to a new private output file using `rb-release-key decrypt SEALED NEW-ARCHIVE`, then inspect the archive before extracting it into an empty private directory. Sharing decrypted material is a separate owner decision; encryption cannot prevent an authorised recipient copying it.

The [manifest](../releases/manifest-0.10.0a1.json) and [ciphertext hash](../releases/SHA256SUMS) identify the release. Check them through a trusted publisher channel: anyone with a public recipient key can encrypt different content, so encryption alone is not publisher authentication. Owner-only builds/tests are described in the native guide and Architect checklist. Public CI validates the distribution and its hashes; it does not pretend to execute an encrypted compiler.
