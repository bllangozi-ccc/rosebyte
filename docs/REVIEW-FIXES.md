# Independent review: findings and corrections

## Recursive typed equality — corrected in reference0.10.1a1

The reviewer found that the Python reference checked only the outer value type. Nested booleans could therefore compare equal to integers: `[true]` versus `[1]` and `{"x":true}` versus `{"x":1}` returned true. The native VM returned false. This could change an application's decision; no exploitation claim is made.

The reviewed correction compares types recursively. Lists preserve order; object key order is irrelevant but key sets and recursively typed values must match. Null remains distinct from false/zero. Depth bounds remain in force. The resulting reference-file hashes match the reviewer's tested candidate exactly. We reproduced original failures separately, then verified the corrected outcomes against the unchanged native VM.

Local expanded verification:58core/native checks and71current hosted checks passed. New tests cover nested boolean/integer equality, reordered objects, null/depth handling and raw versus escaped Unicode SOURCE compilation. The original core release is retained; the encrypted patch supplies the new reference package and evidence. Native binary/wire formats are unchanged. See [implementation](IMPLEMENTATION.md) and [encrypted releases](RELEASES.md).

## Raw Unicode on unpatched json-c0.18 — open

The reviewer reproduced valid raw UTF8 source rejection on json-c0.18 while equivalent Unicode escapes work. Original Root94 json-c0.17 accepts both forms for `é`, `成功` and `🌹`; this does not invalidate the0.18finding. Explicit source-path tests now cover the gap that older tests missed. Upstream tracked a signed-character strict-parser issue in [#875](https://github.com/json-c/json-c/issues/875) and [#892](https://github.com/json-c/json-c/issues/892). A compatibility candidate is under review. Do not disable strict validation or claim unpatched0.18support from the0.17results.

## Review status

The reviewer reports consistent codec baselines/envelope sizes, independent application cases, sanitizer and isolated scanner checks. Those are review evidence for the tested cases, not a completed security certification or general performance superiority. Production scanner freshness is checked separately on Root94. No private conversations, source patches, keys or project data are published here. Further findings remain welcome through the private review workflow.
