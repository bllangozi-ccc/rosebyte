# RoseByte Audit Lens

[Open the tool](https://jacknrose.co.uk/tools/audit-lens) · [Application source, bytecode and tests](https://github.com/bllangozi-ccc/rosebyte/tree/main/examples/audit-lens) · [Ask in chat](https://jacknrose.co.uk/ai-chat) · [All guides](https://jacknrose.co.uk/guide)

Audit Lens is a new RoseByte application for a common developer task: turning saved npm dependency-audit output into a compact, severity-ordered triage report. It is not npm itself, a new vulnerability scanner or a claim that this new tool is already popular.

## Use it

1. On a project you administer, save a report using `npm audit --json > audit.json`. npm may exit nonzero when vulnerabilities are reported; keep and inspect the JSON. The npm audit step contacts your configured registry; Audit Lens does not.
2. Open Audit Lens, register/sign in through RoseByte if needed, then return to the tool. Paste your saved report, choose summary or HTML, and press Run.
3. Review the result and the original report. Download the compact JSON or escaped HTML if useful. Audit Lens never installs, patches or approves a dependency update.

The [official npm audit documentation](https://docs.npmjs.com/cli/v11/commands/npm-audit/) explains what npm checks and how fixes differ from reporting. The [official npm audit report implementation](https://github.com/npm/cli/blob/latest/workspaces/arborist/lib/audit-report.js) defines report version 2. These links are references, not endorsements.

## What runs in RoseByte

The application source is `audit-lens.rbl.json`, compiled by the RB-written compiler to `audit-lens.rblb`. Validation of normalized rows, strict severity/scope/fix typing, duplicate rejection, severity ordering, counts, action labels and escaped HTML rendering execute in RoseByte. The native CLI runs the same bytecode without Python inside the VM.

A small Python adapter parses npm JSON and projects the fields the application needs. Unused CVSS floating-point scores and advisory data do not enter the integer-only RoseByte VM. The web service's adapter, authentication, scanning and process limits are trusted host code, not RoseByte. The hosted endpoint executes only this fixed hash-pinned application, never submitted source or bytecode. Public arbitrary program execution remains disabled.

## Output contract

The summary is `[status, counts, rows]`. Counts are ordered **critical, high, moderate, low, info**. Rows are `[package, severity, isDirect, nextStep]`, ordered by severity with original order retained for ties.

- `review-required`: at least one vulnerable-package record was supplied.
- `no-findings-reported`: the supplied report contains no vulnerable-package records. It does **not** mean the project is safe or the report is current or complete.
- `update-review`, `breaking-change-review`, `manual-review`: review labels derived from npm's saved `fixAvailable` flag; never a promise a fix can currently be installed. Consult the original report for target versions, release-age restrictions, ranges and other conditions.

Only report version 2 is supported. Missing/invalid required fields, unknown severities, duplicate JSON keys, mismatched package names, error reports, non-finite numbers and limits are refused. Explicit `false` differs from `0`. Limits: 65,536 UTF-8 input bytes, 256 package records, 128 UTF-8 bytes per package name. Larger reports need a separately reviewed limit increase, not truncation.

## Measured size and timing

These are synthetic fixtures with no real vulnerability claims. Full results and the reproduction script are in `examples/audit-lens/measurements.json` and `benchmark.py`.

| Fixture | Input JSON | Summary | Reduction | HTML |
|---|---:|---:|---:|---:|
| Two-package sample | 631 B | 130 B | 79.40% | 1,046 B |
| 24-package synthetic report | 17,692 B | 1,438 B | 91.87% | 3,157 B |

This is **lossy field projection**, not a new compression ratio: advisory prose, URLs, installed paths, ranges and unused metadata are omitted. Retain the original. The conventional Python implementation produces identical summary/HTML sizes.

RoseByte source: 6,585 B; bytecode: 3,399 B, **48.38% smaller than its own source**. Python reference: 2,428 B. With zlib9, the artifacts are 1,403 / 1,197 / 1,173 B respectively. Runtime, adapter and dependencies are excluded from these application-only sizes. RoseByte does not beat Python's artifact size in this example.

On the measured Root94 run, the 24-row summary took median 0.0142 ms in the Python reference and 4.4792 ms in the Python-hosted RoseByte VM (100 measured runs each). A fresh native process including the live incoming scan gate took median 21.3444 ms (25 runs). These boundaries differ; the process measurement cannot establish a cross-language speedup. Results depend on hardware, load and scanner state.

## Security measures and tested limits

- The fixed RoseByte application has no filesystem, network, shell, import, eval or package-install primitives. It cannot itself fetch a package or execute an advisory.
- Typed validation rejects malformed policy input. HTML escapes package names; attacker strings are data, not markup. The generated HTML contains no scripts, inline event handlers or untrusted resource URLs and includes a restrictive content policy.
- Reports omit installed paths and advisory prose from output, reducing accidental disclosure when sharing summaries. Package names and severities remain sensitive: share only with permission.
- Hosted requests, decoded reports and results pass the incoming scan gate. Authentication, active-project grants, bounded process time/memory, concurrency admission and final grant rechecks remain enforced. Raw reports are not retained by the application; hash receipts are retained.
- Local CLI report inputs must be regular files; symlinks/FIFOs are refused. Normalized temporary inputs are private and cleaned. The CLI scans the entire original report before parsing and scans the final output; the native runner also scans bytecode and normalized inputs. Missing/rejecting scanner or mismatched size/hash receipts fail closed. The tool verifies its bytecode against the published manifest before running.

Verification: 1,000 generated cases in both output modes matched a separate oracle in the reference VM; 120 cases matched the native VM, with 24 also run under the combined sanitizer build. Tests cover maximum 256-record input, malformed types/duplicates, unknown severity, integer/boolean confusion, empty reports and HTML injection strings. Hosted tests verify authentication, no arbitrary submitted code and revocation after processing. Test scripts are published. The independent review of the underlying 0.10.2a1 runtime predates this application; a separate independent review of Audit Lens has not been completed.

These reduce specific risks; they are not proof of complete safety, safe intent, fresh advisory coverage or security superiority over npm or the Python reference.

## Local use

With an authorised qualified `rosebyte-native` 0.10.2a1 runtime and configured incoming gate:

```sh
cd examples/audit-lens
python3 run.py sample-audit.json
python3 run.py sample-audit.json --format html > report.html
# Optional byte-identical rebuild, choosing a new output filename:
rosebyte-native compile audit-lens.rbl.json rebuilt.rblb
```

The core runtime is owner-encrypted and is not installed by this example. Public users without an authorised runtime can use the hosted tool; the public checkout alone cannot run native VM tests. No credentials are requested by these scripts. Do not download and execute arbitrary runtime replacements from chat.

For adapter/reference smoke tests: `python3 -m unittest discover -s examples/audit-lens -p test_tool.py -v`. VM/native tests explicitly skip without `ROSEBYTE_CORE_SOURCE` pointing to an authorised review checkout. That environment is never fetched automatically. Benchmark/test output must distinguish skipped checks from executed checks.
