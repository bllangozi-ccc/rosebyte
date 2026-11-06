# RoseByte symbol-and-number language (RBS1)

[Try the rebuilt tool](https://jacknrose.co.uk/tools/audit-lens-shorthand) · [Shorthand Audit Lens source](https://github.com/bllangozi-ccc/rosebyte/tree/main/examples/audit-lens-shorthand) · [Dictionary](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/shorthand-dictionary.json) · [Chat](https://jacknrose.co.uk/ai-chat)

**RBS1 is RoseByte's compact authored source syntax.** Outside quoted text, it uses ASCII symbols, decimal numbers and optional spaces. English strings in a report are data, not language keywords. The previous JSON AST is retained as an interchange/debug representation; the original Audit Lens sample remains intact.

Example: add two supplied numbers and return the result:

```text
!1 0:0(0 1){^~0$0$1}
```

With entry arguments `[7,6]`, the result is `13`. No model, OpenAI call, string evaluation or shell is involved.

## Dictionary and rules

- `!1` selects the frozen version-1 syntax. Whitespace follows it, then the entry-function ID.
- `:N(P...) { ... }` defines function N with numeric parameter slots. Function IDs are 0–31; slot IDs are 0–4095. Parameters are separated where numbers would otherwise merge.
- `$N` reads a local slot. `=N expression` declares it; `;N expression` assigns it. A semicolon is assignment, not an end-of-line marker.
- `^expression` returns a value. `?expression{then}{else}` branches. `*N expression{body}` iterates over a bounded list, binding slot N.
- `~N` invokes a primitive using its existing public numeric opcode and fixed arity. Examples: `~0` add, `~5` typed equality, `~11` length, `~13` object get, `~29` HTML escape. The dictionary lists all 30 operations; their meanings are not renumbered.
- `@N(arguments...)` calls function N. `[expressions...]` is a list. `+`, `-`, `_` are true, false and null. Negative integers use `-` followed immediately by digits. A standalone false followed by a positive integer therefore needs a separator.
- Text is quoted using strict JSON string/Unicode escapes. Integers are checked signed 64-bit values. Leading zeros, negative zero, floats, unknown opcodes/versions, comments and trailing garbage are refused.
- `#start,delta,second,count` is an exact numeric-list shorthand. For example `#0,1,2,8` means `[0,1,4,9,16,25,36,49]`. Generation, deltas and every emitted value are checked; count is 0–4096. It is not lossy prediction. Unrepresentable or irregular data stays an ordinary list.
- Whitespace is optional only where token boundaries remain clear. Canonical formatting strips unnecessary whitespace without changing quoted text.

Limits remain: 65,536 source bytes, 65,536 expanded JSON bytes, 32 functions, eight arguments, 4,096 collection items, 16,384 parsed structural nodes and depth 64. Numeric runs charge generated nodes and cannot bypass expansion bounds. Existing VM fuel/memory/output limits and authority rules still apply.

The [machine-readable dictionary](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/shorthand-dictionary.json), [executable dictionary in RoseByte](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/dictionary.rbs) and [hash manifest](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/shorthand-manifest.json) contain the complete mappings and rules. The executable codebook returns 57 version/primitive/syntax/rule rows. It is public semantics, not a credential, secret encryption dictionary or permission grant. Incompatible changes require a new syntax version.

## Compile, run and understand

With the qualified native runtime **0.11.0a1** and incoming gate:

```sh
rosebyte-native compile audit-lens.rbs new-output.rblb
rosebyte-native run new-output.rblb inputs.json
rosebyte-native --check-library
```

The existing RB-written compiler still generates bytecode. The new bounded C/Python frontends parse shorthand into the checked AST; the shorthand parser itself is not claimed to be written in RoseByte. Native compile/run remains Python-independent. Python reference APIs `shorthand.parse`, `shorthand.dumps` and `structured.compile_rb` provide inspection/conversion for authorised core users. `python3 -m rosebyte to-shorthand input.rbl.json new-output.rbs` scans input/output and refuses overwriting.

Conversion canonically renames function/local names to numeric slots, preserving program behaviour rather than original spelling, formatting or comments. Byte-for-byte decompression is measured separately. The hosted translator accepts RBS1 for compilation, but never executes submitted guest programs. The rebuilt Audit Lens page runs only its fixed, pinned reviewed application.

## Storage and delivery results

The preserved Audit Lens JSON source is 6,585 bytes. Its complete RBS1 source is **2,259 bytes**, 65.69% smaller. The conventional Python equivalent is 2,428 bytes. The new compiled bytecode is 3,112 bytes; source size and executable size are separate measurements.

Best compressed application payloads across raw, zlib9, gzip9, bz2-9, LZMA6, Brotli11 and Zstandard19:

| Equivalent application representation | Smallest tested payload |
|---|---:|
| RoseByte RBS1 | **849 B** |
| Existing numeric-slot RBLB1 bytecode | 912 B |
| Python equivalent | 942 B |
| CBOR numeric-slot AST | 1,055 B |
| JSON numeric-slot AST | 1,110 B |

RBS1 is 9.87% smaller than the best tested Python payload and 19.53% smaller than CBOR for this application. Each competing representation received the same compression choices. This does not mean RoseByte invented Brotli or outperforms every compressor on arbitrary data.

Across ten synthetic/real-program fixtures, RBS1 won **9/10** comparisons against the smallest tested alternative representation. Irregular integer data still favoured CBOR. There were **287 exact compression/decompression round trips**; all reconstructed exact representation bytes. JSON/CBOR/RBLB1/RBS1 also reproduced the same alpha-normalized program AST. Results, levels, hashes, losses and single-observation timings are published under the example directory.

Actual existing **authenticated encrypted RBW1 delivery**, balanced profile, with all project checks/scans intact:

| Application source | Complete message packet |
|---|---:|
| RBS1 | **1,708 B** |
| Python equivalent | 1,868 B |
| Original JSON source | 2,214 B |

RBS1 used 8.57% fewer complete packet bytes than Python and 22.85% fewer than the original JSON. All three decoded exactly. TLS/TCP/IP overhead is outside these message counts.

**Cold receiver cost:** the public dictionary is 3,098 bytes, or 1,080 bytes with Brotli11. Charging that dictionary makes the first application payload **1,929 bytes**, versus Python's 942-byte payload without a new dictionary. Delivering it as a separate authenticated RBW1 packet adds 2,112 bytes, making first-use shorthand plus dictionary 3,820 message bytes. Cached/preinstalled dictionary and cold-start results are deliberately separate. Runtime installation costs are excluded for every language. No universal first-use or arbitrary-data victory is claimed.

The logical application is unchanged: unlike the earlier report-size benchmark, these comparisons do not shrink the program by removing validation or security behaviour. They do rename identifiers. The output report still intentionally omits advisory details; see the [original tool guide](AUDIT-LENS.md).

## Safety, tests and remaining work

The shorthand carries no extra authority. Incoming source/output scans, strict UTF-8/Unicode, type checks, integer/expansion bounds, runtime limits, unavailable-scanner failure, existing bans and owner controls remain in force. Existing json-c 0.19 qualification and old-library rejection guard are retained. Syntax/dictionary access does not revoke or control offline copies.

Qualification includes generated arithmetic programs, native/reference bytecode comparisons, Unicode/int64 boundaries, numeric-run overflow/count tests, malformed/truncated/500 mutated sources, sanitizer cases, 1,000 Audit Lens cases in both formats against the preserved sample and an independent oracle, and hosted/UI tests. Exact executed counts are in the release evidence; public CI marks encrypted-core tests skipped when no authorised runtime is available. Independent review of the new frontend is requested separately; the earlier independent 0.10.2a1 runtime review does not cover this new parser.
