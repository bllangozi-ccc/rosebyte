# Security model and reporting

Research preview; independent security review is pending. Finite typed RB
instructions cannot call a shell, import arbitrary code, open network sockets,
write files or loop. A host runner binds a project root and exact read grants.
Source/bytecode is untrusted; validate it before interpreting it.

A bounded language is not an OS sandbox or a proof of benign intent. Host code,
OS permissions, antivirus availability, dependencies and caller controls still
matter. An interpreter written in RB would not automatically make itself tamper
proof. User-controlled output strings must remain data at the consumer.

The downloadable local runner needs a maintained ClamAV daemon and fails closed
on scanner errors. Host-managed filesystem restrictions and current signatures
remain the operator's responsibility. Low-level evaluation APIs operate on
already acquired text and do not make scanner/authority claims by themselves.

The hosted translator uses an isolated `/incoming` broker, account/project grants,
signed requests, encrypted envelopes and a revocation ledger. Detection/reporting
is evidence for investigation, not an oracle of someone's intentions. Keys and
IP addresses do not prove a unique human or a trustworthy agent.

Hosted controls cannot revoke already downloaded source, plaintext or offline
forks. Public chat is not suitable for passwords, keys or project secrets.
No key, private database, conversation history or server credential belongs here.

Report a concern privately to the owner through the hosted account/report flow
at https://jacknrose.co.uk/rosebyte. Do not post exploit payloads or secrets in
public chat/issues. GitHub private vulnerability reporting may be enabled by the
repository owner; do not assume it is enabled before checking.

## Public-source and host boundary

The compiler/interpreter is Python; RB examples contain the application logic.
The public repository can be copied and used offline without a hosted passkey.
No passkey or revocation mechanism can withdraw plaintext already delivered.
The service implementation and production keys/ledgers are not in this repository.
Online hosted keys are not an HSM: compromise of the authorised host process or
root can defeat software controls. Resource-limited codec children are not a
claim that secrets remain safe from a compromised host.

The Linux CLI reads bounded regular source files without waiting on FIFOs and
publishes artifacts atomically without replacement. Other operating systems and
filesystems need separate qualification. An inherited stricter standard-library
CSV limit can still refuse a file; this language does not relax the host's limit.
