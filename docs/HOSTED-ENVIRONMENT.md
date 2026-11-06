# A practical public RoseByte workspace

The public entry points are https://jacknrose.co.uk/rosebyte (translator and
registration), https://jacknrose.co.uk/guide (this guide) and
https://jacknrose.co.uk/ai-chat (help). The JSON API is `/api/rb/`; `/incoming`
is the private scan boundary, not a publicly browsable server directory.

## Current hosted path

1. HTTPS edge applies request/body/connection limits.
2. A human passkey session or agent's signed Ed25519 request proves an account.
   Automation may use an expiring, revocable credential for one private project.
3. Current account/project grants are checked. RoseByte account bans are separate from
   administrator SSH allowances; a shared IP alone does not establish identity.
4. A database-backed lease admits at most one transform per account and two
   concurrently across the service, across threads/processes. Capacity returns
   HTTP 429 with Retry-After rather than waiting indefinitely or duplicating work.
5. Exact request bytes pass the private `/incoming` ClamAV broker. Actual source
   and decoded text are also scanned before release; scanner failure fails closed.
6. A bounded transform child performs allowlisted pack/decode/compile/inspect
   operations. There is no public shell, guest execution or arbitrary URL fetch.
7. Account, project and bearer grants are read again before releasing a result.
   Each admitted request has a hash-only ledger record and a receipt binding its
   input and output. A receipt is not proof of safety, intent or correctness.
8. Crashed requests expire after 120 seconds and are recorded as expired, never
   successful. Child transforms also have CPU, memory and wall-clock limits.

Private data stays scoped to the account/project. Compilation caches are not
shared between public users. Logs/receipts contain hashes, sizes, policy/version
and timings, not submitted source or private credentials. Project keys stay
server-side, encrypted at rest. This does not protect against a compromised root
administrator or replace hardened key custody.

## Abuse and bans

Known-malware signatures reject the exact content and can suspend the authenticated
account for investigation. Scanner outages, unsupported syntax, a timeout or a
resource cap are not evidence of malicious intent and do not automatically ban.
Established-user evidence-bearing reports also create temporary investigation
holds; they are not findings of guilt. Verified findings are required for the
owner's permanent ban/release decision, and deliberately false accusations are
investigated. Account/key/project/session revocation affects hosted use; it cannot
revoke public source, already downloaded plaintext or offline forks.

Existing permanent host IP bans remain in force. SSH administration allowances
and permanent IP bans have one root-managed host registry, with generated scoped
views for each enforcement system. Historical SSH probes remain observations;
they are not silently promoted to permanent bans.

## Before public guest execution

This release intentionally offers no hosted arbitrary program execution. A future
runtime needs a separately qualified per-job sandbox/VM, no network or host files
by default, explicit input/output capabilities, a fresh tenant filesystem,
CPU/fuel/memory/output caps, cancellation, isolated secrets, signed deployment
artifacts and adversarial multi-tenant tests. Scanning alone is insufficient.
Capability imports and memory isolation are established design patterns; see
[Wasmtime's security model](https://docs.wasmtime.dev/security.html).

This is an experimental managed service, not a claim that all malicious programs
or intentions can be identified. Independent security review remains pending.
