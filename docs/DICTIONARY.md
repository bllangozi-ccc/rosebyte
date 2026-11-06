> Core implementation and its complete test harness are private. The encrypted release contains the owner/reviewer build; public readers can use the hosted translator and this specification.

# Public language dictionary

Rosebyte's executable-language dictionary is public, versioned and testable.
Version `2026-11-06.1` defines the current RBL1 primitive opcodes, expression tags,
statement tags, types and limits, plus the RBT2 pipeline instruction dictionary.

- [Readable JSON specification](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/dictionary.json)
- [Dictionary written as an RB program](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/dictionary.rbl.json)
- [Compiled RB dictionary](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/dictionary.rblb)
- [SHA-256 manifest](https://github.com/bllangozi-ccc/rosebyte/blob/main/spec/dictionary-manifest.json)

The RB program returns 53 public codebook rows. Both the native and reference
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
