> Core implementation and its complete test harness are private. The encrypted release contains the owner/reviewer build; public readers can use the hosted translator and this specification.

# RBL1: structured RoseByte and bootstrap

RBL1 adds named functions, checked signed 64-bit integers, booleans, text,
bytes, lists, JSON objects, variables, assignment, conditionals, finite loops,
function calls and pure buffer/text primitives. It is a research dialect alongside
RBT pipelines, not a replacement for the stable RBT1/RBT2/RBB readers.

The syntax is a JSON instruction tree. This deliberately avoids hiding a second,
unqualified textual parser in the bootstrap claim. Example:

```json
{"version":"RBL1","entry":"main","functions":[{"name":"main","params":[],"body":[{"return":{"op":"add","args":[7,6]}}]}]}
```

Compile with the **RB-written compiler**, or run locally after ClamAV inspection:

```sh
python3 -m rosebyte bootstrap-check
python3 -m rosebyte compile-rbl example.rbl.json example.rblb
# inputs.json is [] for the example above
python3 -m rosebyte run-rbl example.rblb --inputs inputs.json
```

`bootstrap/compiler.rbl.json` is the actual RoseByte compiler source. The small Python
`bootstrap/build_source.py` authors that JSON AST; it does not generate bytecode.
The packaged compiler and its source are hash-bound by `manifest.json`.

Stage zero is an independent Python reference compiler. It compiles the RoseByte
compiler once; that RoseByte program compiles its own source again, then a third time.
All three bytecode artifacts must be identical, and match the packaged artifact.
The normal RBL compilation path executes the RoseByte emitter, not the reference
emitter. Input validation and independent decoded-output comparison surround it.

The RoseByte compiler implements instruction selection, function metadata, statement
and expression emission, primitive opcode selection and byte-buffer assembly.
Its fixed primitives offer JSON parsing and byte packing, **not a hidden call to
the Python compiler**. Tests replace the reference emitter with an exception to
check that the production path does not invoke it.

## Deliberate limits

- 65,536 source bytes; 32 functions; 8 arguments per function/call.
- 16,384 syntax nodes; depth/call limit 64; at most 4,096 collection items.
- Checked 64-bit arithmetic; 262,144-byte text/byte buffers.
- At most 2,000,000 evaluated steps; callers may lower this budget.
- Strict bytecode bounds, unknown-opcode and trailing-byte rejection.
- No imports, shell, filesystem, network, native pointers, dynamic host lookup,
  reflection or evaluation of Python/JavaScript.
- `let` declares a function-scoped variable once; `set` updates an existing one.
  Put loop accumulators outside the loop; loop variables restore their old value.

Pure primitives include arithmetic, equality, boolean operations, bounded indexing,
JSON object access, concatenation, UTF-8, byte packing, finite split/join, slicing
and HTML escaping. All guest functions share a single fuel budget.

The hosted translator can compile RBL1 but **does not run submitted programs**.
Its fixed trusted RoseByte compiler runs inside the existing bounded transform process.
Local execution is an explicit separate command with scanned input; the runtime
itself is still a trusted Python implementation. This is compiler self-hosting,
not a claim that TLS, passkeys, crypto, the VM or the whole website are written in RoseByte.

## A small complete RoseByte application

`examples/release-check.rbl.json` uses two functions, conditionals, looping and
accumulators to validate bounded release-test reports. It returns `ready` only
if all reports passed and had nonnegative durations; otherwise `needs_work`.
Its application logic is RoseByte, not a Python command hidden behind an RoseByte wrapper.

```sh
python3 -m rosebyte compile-rbl examples/release-check.rbl.json release-check.rblb
python3 -m rosebyte run-rbl release-check.rblb --inputs examples/release-inputs.json
# {"result": ["ready", 3]}
```

These are synthetic reports and a pure decision result, not a deployment grant.

## Native toolchain and dictionary

RBL1 also runs on the [native runtime](NATIVE.md), independently of Python.
The [public dictionary](DICTIONARY.md) includes an RB-written executable codebook.
The web service and Python reference interpreter remain separate implementations.
Native/reference object keys exclude NUL; floats remain outside the language.


## Typed equality

`eq` compares value types recursively. Boolean `true` differs from integer `1`, including inside lists and objects; `false` differs from `0`. Lists compare in order. Objects require identical key sets and recursively equal values; key insertion order does not matter. Null equals null only. Equality remains subject to the language depth/resource bounds.
