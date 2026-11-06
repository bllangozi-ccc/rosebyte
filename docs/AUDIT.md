> Core implementation and its complete test harness are private. The encrypted release contains the owner/reviewer build; public readers can use the hosted translator and this specification.

# Language audit — 6 November 2026

Historical baseline: **0.8.0a1** (current native qualification: **0.10.0a1**) — see [the follow-up findings and current results](#v08-follow-up-audit).

This preview fixes reproducible language/runtime faults. The before/after audit
used disposable files and keys, never the real owner vault. No old Rose worker
or model was started. These are bounded tests, not independent certification.

## Findings and corrections

| Finding | Correction |
|---|---|
| A CSV field of 4,098 UTF-8 bytes could pass a 4,096-byte documented limit when characters were multibyte | Explicit encoded-byte checks |
| Missing columns could pass when the CSV had no rows | Retain and validate the header before evaluating referenced columns |
| A missing right-hand condition column could be hidden by a matching left branch | Validate both referenced columns independently of row truth values |
| `-0` was accepted as a canonical decimal integer | Reject negative zero; preserve exact integer arithmetic |
| Direct source parsing had no early byte bound | Check source type and UTF-8 size before tokenisation/JSON parsing |
| A direct evaluator call could exceed the file input bound | Apply the same byte bound at evaluator entry |
| Source and legacy decoding did not consistently reject NUL file paths | Shared validation after either bytecode format is decoded |
| Boolean transform values were accepted as integers | Require an actual integer type for the bounded transform varint |
| The historical single-request runner could return after a project was revoked during file scanning | Recheck policy and runtime identity before completing/returning the result |

Filesystem execution already rejected the invalid NUL paths. The correction
moves rejection earlier and makes parser/compiler/decoder behaviour consistent.
The revocation fix applies to the full lab runtime, not to the downloadable
finite compiler alone. Hosted accounts still cannot execute submitted code.

## Verification

- Full updated lab regression: **116 checks passed** (includes existing tests,
  the targeted reproductions and the property-test methods).
- Independent CSV result calculation: **1,200 generated pipelines** checked for
  exact filtering, grouping, sorting, sums, minima/maxima and rational means.
- **60,000 deterministic bytecode mutations**: rejected or decoded to a valid,
  recompilable program. Accepted mutations are not claimed to preserve the
  original program: they must preserve their own decoded semantics.
- **69 exact codec/profile round trips**, including Unicode, random bytes and
  polynomial data; **120 baseline/structural cases** with corruption checks.
- Expansion bombs rejected in resource-limited codec children; a subsequent
  clean decode succeeds. Traversal, symlinks and FIFO reads are refused.
- Public standard-library package: **15 tests passed**, including its own
  generated/mutation cases. These overlap with the lab generators; do not sum
  the counts as if they were different independent campaigns.
- Real local ClamAV + RB-written quality-reports application: expected exact
  results from the provided synthetic CSV, with shared scanned file snapshots.
- Hosted service's **40 existing regression tests passed** after the forward
  kernel update. Real public HTTPS compilation accepts the RoseByte example, rejects
  its invalid-path test and reports `authority_granted: false`.

Historical test fixtures emitted resource-cleanup warnings; those are retained
in the private test logs, not silently classified as a new runtime failure or
proof of leaked live workers. No broad performance improvement is claimed from
this correctness audit. No independent external security review has occurred.

## Remaining boundaries

The grammar is deliberately small. Public web-service orchestration, passkeys,
TLS, process isolation and cryptography remain implemented by maintained host
components. RoseByte's example application logic is genuinely RoseByte, but this interpreter
is implemented in Python. Offline code and decoded plaintext cannot be revoked
by a hosted access key. Antivirus and static checks cannot prove good intent.

## v0.8 follow-up audit

Current preview: **0.8.0a1**. The initial v0.7 findings above remain historical
context; the following fixes and results supersede its current test counts.

| Further reproduced fault | Fix |
|---|---|
| A reused parsed CSV could be paired with different source text | Bind the reusable snapshot to the exact source digest |
| A result consumer could modify rows shared with a later report | Read-only parsed rows and detached emitted results |
| Parsing changed a process-global CSV setting | Enforce byte limits locally without changing that setting |
| Valid long quoted operands failed the batch source round trip | Distinguish compiled size from source size, retaining both bounds |
| Direct validation accepted a program too large to compile | Apply the exact bytecode bound consistently during validation |
| The local source reader could block on a FIFO | Nonblocking regular-file reads, bounded before reading |
| A failed artifact write could leave partial output | Publish a fully written file atomically, without overwriting targets |
| A trickling scanner could extend a series of per-read waits | One absolute deadline across connect, send and receive |
| Malformed CSV leaked a parser-specific exception through the CLI | Return a controlled language error |
| Lab package build/decode could return after a mid-operation policy change | Recheck the policy version before returning packet/plaintext |

### Current verification

- **119 lab checks passed**, including three new disposable-key policy races.
- **31 public-package tests passed**, including 128 parallel snapshot-use cases,
  actual FIFO refusal, symlink/output preservation, JSON compatibility and an
  eight-report escaped-source/binary/source round trip.
- The generated **1,200 CSV / 60,000 bytecode mutation** campaigns continue to
  pass. They are included in the method counts and overlap across packages.
- The real local ClamAV scan gate and RB-written example application pass.
- The actual hidden-prompt lab CLI creates/verifies an encrypted disposable
  vault without echoing its synthetic secret. No real owner vault is used.
- The actual signed/encrypted batch-compute CLI passes cold and warm execution:
  three cold evaluations, three warm cache hits, one fresh warm input scan,
  equal verified results and a verified latency-profile result.
- Hosted regression checks and public HTTPS compilation/inspection are recorded
  with the deployment evidence. No new execution authority is offered publicly.

An intermediate read-only snapshot implementation broke an existing JSON
compatibility check. The full suite caught it before release; the corrected
read-only representation preserves JSON encoding and has a regression test.
Historical test-fixture cleanup warnings remain recorded rather than hidden.

This completes this internal audit pass over the finite language, bytecode,
local runner, scoped-file path, codec limits and tested package-policy paths.
It does not constitute an independent security review, a formal proof, testing
of every operating system or a claim that all future defects are eliminated.
The low-level APIs are part of a trusted host runtime, not a boundary against a
malicious host process. Local filesystem hardening is qualified on Linux.

## 0.9 structured-language qualification

- RB-written emitter compiles its own source over three byte-identical stages.
- 250 deterministic generated arithmetic programs compare the RoseByte emitter with
  the independent reference emitter and separately computed expected answers.
- Fuel/call-depth/buffer/type/integer overflow, malformed source and all bytecode
  truncations of a fixture are tested. Host codegen is disabled in a production
  emitter test. These checks do not certify the Python VM or prove broad language
  completeness. Hosted arbitrary guest execution remains disabled.
- Hosted-only tests additionally cover account/project isolation, concurrency
  admission, stale request expiry, unavailable AV, matched scan receipts and
  mid-operation account/project/token revocation.
