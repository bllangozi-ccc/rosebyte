> Core implementation and its complete test harness are private. The encrypted release contains the owner/reviewer build; public readers can use the hosted translator and this specification.

# RoseByte dictionary

**Short codes, shared meanings, fewer bytes.** Simplify → compile → compress.

Public entry: [jacknrose.co.uk/dictionary](https://jacknrose.co.uk/dictionary). Short codes carry fixed meanings; the dictionary supplies the readable names. Arguments and actual implementations are still required.


RoseByte's executable-language dictionary is public, versioned and testable.
Version `2026-11-06.1` defines the current RBL1 primitive opcodes, expression tags,
statement tags, types and limits, plus the RBT2 pipeline instruction dictionary.

- [Readable JSON specification](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/dictionary.json)
- [Dictionary written as an RoseByte program](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/dictionary.rbl.json)
- [Compiled RoseByte dictionary](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/dictionary.rblb)
- [SHA-256 manifest](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/dictionary-manifest.json)

The RoseByte program returns 53 public codebook rows. Both the native and reference
runtimes must return identical rows. The native primitive-name/arity table is
reproducibly generated from the same public specification and checked alongside
compiler self-bootstrap and differential primitive tests.

```sh
printf '[]\n' > empty-inputs.json
rosebyte-native run spec/dictionary.rblb empty-inputs.json
# Returns the 53 public version/opcode rows after incoming scans.
```

`python3 tools/build_dictionary.py` reproduces the public dictionary artifacts;
the native runtime does not need Python to consume or execute them. Generation
is a development task, distinct from runtime use. Changes must preserve assigned
opcode meanings; incompatible changes require a new bytecode format/version,
not silent renumbering of the existing codebook. Artifact manifests bind exact
bytes. A hash detects accidental mismatch; it is not an independent publisher
signature or a substitute for trusted release distribution.

This is a **language codebook**, not an encryption key, permission grant or proof
of good intentions. It contains no account credentials, project data or vault
contents. Project-specific compression dictionaries can reveal vocabulary and
remain private unless their owner deliberately publishes them. No private
compression dictionary was used to produce these public files.

## Primary symbol-and-number source

See [RBS1 syntax and rules](SHORTHAND.md), `spec/shorthand-dictionary.json`, `spec/dictionary.rbs` and `spec/shorthand-manifest.json`. Primitive IDs retain the codebook meanings above. The older RBL1 JSON artifacts remain compatible and unchanged. RBS1 provides the compact authored form; quoted strings remain literal data.

## Common commands as RoseByte codes

These use the existing frozen RBS1 dictionary. They are working syntax, not invented abbreviations. Each example passed native and reference compilation/execution with matching outputs and native input/output scans.

- add: `~0` (2 ASCII bytes for the operation token). Full 20-byte example: `!1 0:0(0 1){^~0$0$1}`; input `[7,6]`; output `13`.
- sub: `~1` (2 ASCII bytes for the operation token). Full 20-byte example: `!1 0:0(0 1){^~1$0$1}`; input `[7,6]`; output `1`.
- mul: `~2` (2 ASCII bytes for the operation token). Full 20-byte example: `!1 0:0(0 1){^~2$0$1}`; input `[7,6]`; output `42`.
- div: `~3` (2 ASCII bytes for the operation token). Full 20-byte example: `!1 0:0(0 1){^~3$0$1}`; input `[12,3]`; output `4`.
- mod: `~4` (2 ASCII bytes for the operation token). Full 20-byte example: `!1 0:0(0 1){^~4$0$1}`; input `[13,5]`; output `3`.
- eq: `~5` (2 ASCII bytes for the operation token). Full 20-byte example: `!1 0:0(0 1){^~5$0$1}`; input `[7,7]`; output `true`.
- lt: `~6` (2 ASCII bytes for the operation token). Full 20-byte example: `!1 0:0(0 1){^~6$0$1}`; input `[3,7]`; output `true`.
- len: `~11` (3 ASCII bytes for the operation token). Full 17-byte example: `!1 0:0(0){^~11$0}`; input `[[1,2,3]]`; output `3`.
- at: `~12` (3 ASCII bytes for the operation token). Full 21-byte example: `!1 0:0(0 1){^~12$0$1}`; input `[[4,5,6],1]`; output `5`.
- get: `~13` (3 ASCII bytes for the operation token). Full 21-byte example: `!1 0:0(0 1){^~13$0$1}`; input `[{"key":"value"},"key"]`; output `"value"`.
- concat: `~16` (3 ASCII bytes for the operation token). Full 21-byte example: `!1 0:0(0 1){^~16$0$1}`; input `["hello ","world"]`; output `"hello world"`.
- append: `~17` (3 ASCII bytes for the operation token). Full 21-byte example: `!1 0:0(0 1){^~17$0$1}`; input `[[1,2],3]`; output `[1,2,3]`.
- parse_json: `~20` (3 ASCII bytes for the operation token). Full 17-byte example: `!1 0:0(0){^~20$0}`; input `["[1,2]"]`; output `[1,2]`.
- slice: `~26` (3 ASCII bytes for the operation token). Full 25-byte example: `!1 0:0(0 1 2){^~26$0$1$2}`; input `["abcdef",1,4]`; output `"bcd"`.
- split: `~27` (3 ASCII bytes for the operation token). Full 21-byte example: `!1 0:0(0 1){^~27$0$1}`; input `["a,b",","]`; output `["a","b"]`.
- join: `~28` (3 ASCII bytes for the operation token). Full 21-byte example: `!1 0:0(0 1){^~28$0$1}`; input `[",",["a","b"]]`; output `"a,b"`.
- html_escape: `~29` (3 ASCII bytes for the operation token). Full 17-byte example: `!1 0:0(0){^~29$0}`; input `["<x>"]`; output `"&lt;x&gt;"`.
- declare, assign and return: `=N ;N ^`. Full 25-byte example: `!1 0:0(){=0 5;0~0$0 1^$0}`; input `[]`; output `6`.
- branch: `?`. Full 27-byte example: `!1 0:0(0){?~6$0 0{^-1}{^1}}`; input `[-5]`; output `-1`.
- sum a list with a finite loop: `*N`. Full 32-byte example: `!1 0:0(0){=1 0*2$0{;1~0$1$2}^$1}`; input `[[1,2,3]]`; output `6`.
- call a defined function: `@N`. Full 32-byte example: `!1 0:0(0){^@1($0)}:1(0){^~2$0 2}`; input `[7]`; output `14`.
- exact quadratic number list: `#`. Full 19-byte example: `!1 0:0(){^#0,1,2,8}`; input `[]`; output `[0,1,4,9,16,25,36,49]`.

The [machine-readable examples](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/common-commands.json) bind the exact dictionary hash. Common primitive meanings are built into the qualified compiler/runtime: the whole dictionary does not need downloading for every command. A short reference does not create an implementation, grant filesystem/network access or request model reasoning. Experimental bookmarks for larger reusable blocks remain separate and are not yet a deployed language import feature.
