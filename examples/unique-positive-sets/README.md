# Built-in sets, RBS2 / runtime0.12.0a1

The existing unique-positive-sum task now uses built-in stable deduplication instead of a nested scan. `sum.rbs` is46 bytes and compiled output118 bytes. Existing arguments remain one list wrapped in an argument list. Example `[[3,-2,3,7,0,7,1]]` returns11.

Compared with the preserved Architect89-byte source/223-byte executable, the new source and bytecode are smaller. Its Brotli11 source payload is48 bytes versus75. The original70-byte Python function compresses to69; a compact35-byte anonymous Python lambda compresses to39 and still wins. `measurements.json` retains both comparisons. The compact-reference.py file adds a binding/final newline; its total file length differs from the unbound lambda expression measured in the JSON.

Both RoseByte functions passed1007 oracle cases. Same-runtime reference execution on256 integers/128 unique values measured11 samples: median45.456ms before and0.818ms after, excluding compile and scanning. This is not native-vs-Python throughput, network speed or a universal gain. The core suite covers stable scalar sets, mixed bool/int identity, Unicode/bytes,1000 generated operation cases, native/sanitizer paths,4096-item bounds and fuel. Public hosted compilation does not execute submitted programs.

The dictionary meanings are installed with a compatible runtime. Missing codebooks, runtime installation, authentication/encryption and cache misses add real costs. Original !1 programs and opcode meanings remain unchanged. !2 and new bytecode operations require0.12.0a1; older engines reject them. See https://jacknrose.co.uk/dictionary and https://jacknrose.co.uk/ai-chat .
