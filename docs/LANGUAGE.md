> Core implementation and its complete test harness are private. The encrypted release contains the owner/reviewer build; public readers can use the hosted translator and this specification.

# Rosebyte 0.7 finite-pipeline language reference (experimental)

A tool is a bounded sequence of 2–16 instructions. It starts with `read` and ends with `emit`. Source is UTF-8, one instruction per line; `#` comments are recognised outside quoted operands. Strings use JSON double-quote/escape rules. No interpolation, shell parsing, `eval`, arbitrary imports, dynamic calls or loops are provided. Canonical JSON instruction arrays are also accepted; duplicate object keys are refused.

Typed operations:

| Instruction | Input | Output | Meaning |
|---|---|---|---|
| `read "path"` | Initial state | Text lines | Read one project-granted, scoped UTF-8 regular file |
| `find "text"` | Lines | Lines | Literal substring filter |
| `csv` | Immediately after read | CSV rows | Strict header/column checks |
| `where-any "field1" "op1" "value1" "field2" "op2" "value2"` | CSV rows | CSV rows | Either condition may match |
| `group-stats "group-field" "integer-field"` | CSV rows | Aggregates | Count, sum, minimum, maximum and exact rational mean per group |
| `sort-by "field" "asc-or-desc"` | Aggregates | Aggregates | Stable sort by group/count/sum/min/max |
| `limit N` | Lines/rows/aggregates | Same | First 1–100 results |
| `emit` | Any valid result | Terminal | Return data, never execute it |

Comparisons are eq/ne for strings or gt/ge/lt/le for bounded canonical decimal integers. Numeric operands and fields have at most 18 decimal digits; integer arithmetic is exact. Aggregates never divide by zero; empty input yields an empty result. Means are represented by numerator and denominator, avoiding rounding claims. Values beginning with spreadsheet formulas or instructions remain data, not commands.

Bounds: 64 KiB input file, 4096 physical lines/rows, 32 CSV columns, 4096-byte CSV fields, 256 groups, 512 UTF-8 bytes per string operand, 4096-byte compiled program. Symlinks, traversal, ambiguous paths and ungranted files are denied. Bound project root and current grants are checked by the package runner before the VM. The local runner scans source and file bytes through its configured ClamAV Unix socket. Hosted requests go through the hosted /incoming gate. Parsing does not modify the process-global CSV field limit. Reusable snapshots retain read-only rows and the exact source digest; emitted results are detached copies.

RBT2 bytecode: `RBT2` magic, one-byte instruction count, then opcode and operands. String operands use a big-endian uint16 length followed by exact UTF-8 bytes; limit uses one byte. Opcodes: read=1, find=2, limit=3, emit=4, csv=5, where_any=6, group_stats=7, sort_by=8. Trailing bytes, unknown tags, truncations, nonconforming types and invalid operation order fail. The older four-operation search shape continues to compile to compatible RBT1 bytes.


## Named batches

A UTF-8 JSON object containing one `reports` list defines 1–8 reports. Each has
a unique lowercase identifier `name` and an RB `source` string. The compiler
produces RBB1 framing around the independently checked RBT programs. Names are
1–32 ASCII characters matching `[a-z][a-z0-9_]*`. Trailing bytes, duplicate names,
unknown opcodes and truncated operands are rejected. See examples/quality-reports.json.

## Audit bounds

Source and evaluator text are bounded to 65,536 UTF-8 bytes before parsing. CSV
fields are limited to 4,096 UTF-8 bytes. Referenced columns must exist, including
for empty tables and short-circuited conditions. Negative zero is not canonical;
use `0`. NUL paths are rejected in source and legacy bytecode.

The public package contains the RBT1/RBT2/RBB1 finite compiler and interpreter.
Historical RB01/RB02/RB03 encrypted-package research and the hosted RBW1 envelope
are separate protocols, not exported compiler functions. Hosted encoding does
not give a registrant filesystem or execution authority.

## v0.8 source and snapshot rules

The 4,096-byte compiled-program limit also applies during direct validation.
Individual report source is bounded to 65,536 UTF-8 bytes; the enclosing named
batch JSON is bounded to 262,144 bytes. These separate bounds preserve canonical
round trips even when quoted operands need more source bytes than bytecode.

Reusable CSV snapshots retain their header and source digest. Passing a snapshot
for different text is rejected. Supported snapshot APIs are read-only and retain
JSON compatibility; emitted data is detached and can be changed by the consumer
without changing later reports. These are trusted-runtime API integrity checks,
not a security boundary against a hostile Python host.
