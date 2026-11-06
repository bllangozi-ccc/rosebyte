# Independent Architect qualification

Status: **scoped independent 0.10.2a1 retest completed and accepted, 6 November 2026**. No new failing case was found in that retest. This is not whole-system security certification or an endorsement. See [findings and corrections](REVIEW-FIXES.md) for results and limits. The checklist below remains available for further review.

First obtain an owner-authorised decrypted core release in a private review environment; the public checkout alone cannot run core tests. Verify its manifest/hash and preserve confidentiality.

Review a pinned Git commit, record compiler/libjson-c/OpenSSL/OS versions and
hash the source/artifacts before testing. No owner passkey, server credential,
project encryption key, live database, private chats or Root94 shell access is
needed for the source-level tests. Work on your own isolated test machine.

1. Audit the RBL1 grammar, public dictionary and binary decoder; look for divergent
   opcode/arity mappings, ambiguous integer/UTF-8 handling and duplicate fields.
2. Rebuild with warnings-as-errors. Run all tests, ASan and UBSan; independently
   generate programs and malformed bytecode beyond the supplied deterministic set.
3. Reproduce RoseByte compiler self-bootstrap. Compare native/reference bytecode and
   behaviour for arithmetic, Unicode, functions, loops, buffers, JSON and errors.
4. Verify real release binaries do not have the testing scanner bypass. Trace
   execution with Python absent and inspect linked libraries and subprocesses.
5. Inspect integer/length overflow, allocation lifetime/error cleanup, recursion,
   fuel, stack, CPU/memory/time guards and output/file atomicity under interruption.
6. Separately review the native incoming adapter: peer credentials, partial
   frames, size limits, scanner freshness/unavailability, EICAR rejection, hash
   binding, audit hold, permissions, log rotation and service resource isolation.
7. Check tenant/security assumptions. Hosted arbitrary guest execution remains
   disabled; do not infer multi-tenant isolation from the local VM tests alone.
8. Report reproducible findings and minimal inputs, severity, exact source/build,
   expected/observed behaviour and remaining unanswered questions. Do not merely
   rerun supplied success cases or certify intent detection from antivirus results.

A failing test is a useful finding. Do not use real malware, credentials, live
projects, external targets or production scanning endpoints for fuzz campaigns.
Provide a reviewed repair patch and repeat original acceptance checks before
accepting a fix. Publish only non-sensitive reproduction details.
