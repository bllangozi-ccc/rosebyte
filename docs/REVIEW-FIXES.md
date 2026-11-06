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

Previously corrupted output cannot be reconstructed without the original source. Recompile affected source with the qualified runtime; no historical tasks or artifacts are replayed automatically. Upstream reports:[json-c#875](https://github.com/json-c/json-c/issues/875),[#892](https://github.com/json-c/json-c/issues/892). Final independent retesting of this update is requested; no security certification is claimed.

## Review status

The reviewer reports consistent codec baselines/envelope sizes, independent application cases, sanitizer and isolated scanner checks. Those are review evidence for the tested cases, not a completed security certification or general performance superiority. Production scanner freshness is checked separately on Root94. No private conversations, source patches, keys or project data are published here. Further findings remain welcome through the private review workflow.
