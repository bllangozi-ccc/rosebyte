# Independent review: findings and corrections

## Recursive typed equality — corrected in reference0.10.1a1

The reviewer found that the Python reference checked only the outer value type. Nested booleans could therefore compare equal to integers: `[true]` versus `[1]` and `{"x":true}` versus `{"x":1}` returned true. The native VM returned false. This could change an application's decision; no exploitation claim is made.

The reviewed correction compares types recursively. Lists preserve order; object key order is irrelevant but key sets and recursively typed values must match. Null remains distinct from false/zero. Depth bounds remain in force. The resulting reference-file hashes match the reviewer's tested candidate exactly. We reproduced original failures separately, then verified the corrected outcomes against the unchanged native VM.

Local expanded verification:58core/native checks and71current hosted checks passed. New tests cover nested boolean/integer equality, reordered objects, null/depth handling and raw versus escaped Unicode SOURCE compilation. The original core release is retained; the encrypted patch supplies the new reference package and evidence. Native binary/wire formats are unchanged. See [implementation](IMPLEMENTATION.md) and [encrypted releases](RELEASES.md).

## Unicode decoder qualification — fixed in native0.10.2a1

The reviewer found raw UTF8 source rejection with json-c0.18. Further tests also reproduced silent supplementary-escape replacement in0.17and0.18. For example, escapedU+AD8E3 becameU+FFFD. The corrected release uses the maintained json-c0.19 decoder in a pinned release-local library, leaving the operating system library unchanged. STRICT and UTF8 validation remain enabled. An experimental normaliser was rejected before deployment because it retained the corruption.

An isolated single-scalar decoder probe checked every Unicode scalar as an escaped JSON string and every permitted scalar as raw JSON string content. This tests library string decoding, not all possible programs or a security proof:

| json-c | Escaped scalars tested | Escaped mismatches | Raw scalars tested | Raw mismatches/rejections |
|---|---:|---:|---:|---:|
|0.17|1112064|32768|1112030|0|
|0.18|1112064|32768|1112030|1111936|
|0.19|1112064|0|1112030|0|

Native qualification additionally passed60core/native checks including sanitizers,220raw/escaped compile-and-run cases covering110seededvalues with identical bytecode/results, a60000byte rawtext boundary and18malformedJSON rejection cases. Fourteen real installed-CLI cases passed/incoming and matched the independent reference exactly. Three-stage compiler bootstrap remains byte-identical.

Every compile/run/bootstrap now tests its loaded JSON library for the known raw/supplementary failures. `rosebyte-native --check-library` exposes that check; `--version` reports the loaded version. Unqualified decoders fail before processing user programs. The release-local package was authenticated with signed Debian archive metadata, scanned through/incoming and hash-pinned; third-party licence notices are included. Qualified binary platform:Linuxx86_64/glibc>=2.38, testedUbuntu24.04. Other platforms require their own maintained compatible library/build and qualification.

Previously corrupted output cannot be reconstructed without the original source. Recompile affected source with the qualified runtime; no historical tasks or artifacts are replayed automatically. Upstream reports:[json-c#875](https://github.com/json-c/json-c/issues/875),[#892](https://github.com/json-c/json-c/issues/892). Independent retesting of this update passed within the scope recorded below; no security certification is claimed.

## Review status

The reviewer reports consistent codec baselines/envelope sizes, independent application cases, sanitizer and isolated scanner checks. Those are review evidence for the tested cases, not a completed security certification or general performance superiority. Production scanner freshness is checked separately on Root94. No private conversations, source patches, keys or project data are published here. Further findings remain welcome through the private review workflow.

## Independent 0.10.2a1 retest — accepted 6 November 2026

The reviewer verified the delivered archive hash, used a fresh original source copy, rebuilt with warnings treated as errors and reported no new failing case in this bounded retest:

- 60 supplied core/native tests passed.
- A separately authored corpus passed 220 raw/escaped Unicode compile-and-execute cases; native and reference bytecode/results matched. Original raw UTF-8 and supplementary-escape failures no longer reproduced.
- 1,000 application cases matched both implementations and a separate oracle; eight invalid/overflow cases were rejected.
- 19 malformed JSON cases were rejected. A 60,000-byte raw UTF-8 value returned exactly.
- Separate ASan and UBSan builds each ran 648 malformed/valid bytecode cases without sanitizer diagnostics.
- The supplied exhaustive single-scalar decoder probe was replayed independently: 1,112,064 escaped and 1,112,030 permitted raw scalar cases had zero mismatches with release-local json-c 0.19. This was a replayed supplied probe, distinct from the independently authored 220-case VM corpus.
- Bootstrap, release-library resolution and rejection of injected known-bad json-c 0.18 passed.
- Sixteen isolated scanner/production-binary fixture checks passed, including unavailable-scanner and wrong-peer rejection.

Limits: the scanner fixture used a custom local EICAR signature and synthetic freshness marker; it does not qualify production signature freshness. The reviewer did not independently repeat Debian APT signature-chain retrieval, test the current hosted deployment or establish whole-server safety. Compiler/platform differences produced an environment-specific binary hash; the delivered library ELF hash matched. No new speed or compression advantage is claimed from these correctness tests. Full logs and private review source remain confidential.
