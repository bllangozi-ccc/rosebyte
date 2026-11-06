# What is written in RoseByte?

| Component | Implementation | Verified boundary |
| --- | --- | --- |
| RBT quality gates and benchmark summary | RoseByte pipeline source | Compiled, bounded evaluation and independent result checks |
| RBL1 compiler emitter | RBL1 source | Three-stage byte-identical self-compilation; independent compiler corpus |
| RBL1 structured examples | RBL1 | Pure function/loop/buffer execution checks |
| RBL1 reference VM and independent reference compiler | Python | Separate oracle; resource/type/bytecode tests |
| Native RBL1 VM and incoming adapter | C with maintained libraries | Native self-bootstrap, differential tests and real AV checks; independent review pending |
| Older RBT pipeline compiler/runtime | Python | Existing compatibility and differential tests |
| Website, HTTP, scanning adapter, identities, crypto and key custody | Maintained host libraries/Python | Separate hosted controls; not rewritten in RoseByte |

The normal RBL1 compiler path executes the actual RB-written compiler. Its
primitives do not expose a call to the Python reference compiler. The RoseByte compiler
compiles itself into the same bytecode over three stages. Read
[the specification and reproducible commands](STRUCTURED.md).

This establishes a working self-hosted compiler **on both native and Python reference VMs**, not an
entire RB-built operating system or website. Cryptography, TLS and passkeys remain
maintained host facilities. A language cannot prove good intentions or make itself
uncopyable merely by writing its interpreter in its own syntax.

## Can someone copy the core without the owner secret?

The current public repository contains guides, specifications, examples and an encrypted core release. Its fresh history does not contain the plaintext core. Only the owner-controlled private release recipient can decrypt that release; its private key is wrapped with the owner's existing secret, entered locally through a hidden prompt. The original owner vault is unchanged.

This protects the current release at rest. It cannot retract source that was published earlier, prevent an authorised recipient copying decrypted code, or stop a compromised host inspecting running code. Public specifications and examples remain readable. Passkeys protect hosted identities separately; a biometric is not embedded in the source. Encryption is not a software licence or proof of publisher identity.

The native compiler/runner does not require Python. See [the native guide](NATIVE.md) and [release handling](RELEASES.md).
