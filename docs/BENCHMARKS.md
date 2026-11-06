# Measured compression facts — 6 November 2026

This is an internal, seeded synthetic benchmark, not independent verification or a universal superiority claim. All 120 fixture/method pairs passed exact lossless round trips. Twelve fixtures cover greetings, numeric sequences, JSON, source-shaped text, prose, Unicode and entropy. Each method used two warmups and eleven measured iterations in a fresh process. No compression dictionary was used. Full timings, CPU, peak process RSS, hashes and common authenticated-envelope sizes are in [the JSON report](../benchmarks/results-20261106.json); original fixture bytes are [available](../benchmarks/fixtures).

Baselines: zlib 6/9, Brotli 5/11, Zstandard 3/19. RB profiles select maintained codecs or an exact structural transform; selecting an existing codec does not make it a new entropy coder. The best baseline below means the smallest payload among those six settings, without pretending their CPU costs are equal.

**RB balanced: 2 smaller payloads, 1 tie, 9 larger payloads against those high-density baselines. It does not currently beat existing codecs generally.** Against only zlib6/Brotli5/Zstd3 it had two wins and ten ties. One win is a 17-byte greeting sent raw to avoid compression expansion; raw transmission is available to everyone. The other is a specific numeric sequence, not general-purpose evidence.

| Fixture | Source B | RB balanced B | Smallest baseline (B) | RB encode median ms | Best-size baseline encode ms |
|---|---:|---:|---|---:|---:|
| short-greeting | 17 | 17 | brotli-5 (21) | 0.0589 | 0.0082 |
| squares-2000 | 14537 | 54 | zstd-19 (5210) | 0.9679 | 1.9746 |
| irregular-integers-2000 | 19797 | 9025 | brotli-11 (8615) | 2.7906 | 9.1638 |
| json-lines-8192 | 8192 | 514 | brotli-11 (414) | 0.1468 | 7.1145 |
| json-lines-65536 | 65536 | 3279 | brotli-11 (2422) | 1.1313 | 70.5280 |
| json-lines-262144 | 262144 | 13213 | brotli-11 (9160) | 4.2282 | 297.1960 |
| base64-entropy-4096 | 4096 | 3090 | brotli-5 (3090) | 0.0915 | 0.0351 |
| base64-entropy-65536 | 65536 | 49182 | brotli-11 (49172) | 2.1035 | 40.5513 |
| base64-entropy-262144 | 262144 | 196656 | brotli-11 (196629) | 9.4820 | 163.4840 |
| generated-source-65536 | 65536 | 7835 | zstd-19 (5669) | 2.2279 | 19.7025 |
| generated-docs-65536 | 65536 | 2776 | brotli-11 (1939) | 1.3087 | 78.0224 |
| unicode-records | 18156 | 1355 | brotli-11 (923) | 0.4069 | 17.0827 |

The JSON retains all RB latency/smallest profiles and every baseline, rather than only the winning rows. Selection often adds CPU time; smaller bytes do not imply faster execution. Timing results are local CPU measurements, not network throughput or AI-token savings. Peak RSS includes the Python interpreter and loaded libraries. The same BENCH-AEAD-1 authenticated envelope was used for every method, including nonce, tag, signature and JSON; it is not the production RBW1 protocol. Decoder installation costs are excluded equally. Public opcode dictionaries are language specifications, not compression dictionaries.

The native language bootstrap tests and codec benchmark measure different things. No before/after performance gain from native execution is inferred from this compression run. Further improvements need representative workloads, reproducible measurements and independent review.
